from dataclasses import dataclass
from logging import getLogger
from typing import Callable, List, Tuple

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from controllers.base import BaseController
from views.base import UserInputResult

MAX_CLICK_SHOW_MORE = 50

log = getLogger(__name__)


@dataclass
class StudioData:
    price: int
    footage: int
    name: str
    link: str


class PhotoPlaceProController(BaseController):
    """ https://photoplace.pro/moscow """

    def __init__(self, requirements: UserInputResult):
        super().__init__()
        self.TIMEOUT = 3
        self.result = set()
        self.requirements = self.check_requirements(requirements)
        self.base_url = 'https://photoplace.pro'
        self.search_url = self._get_search_url()

    def find_studios(self) -> List[Tuple[str]]:
        try:
            self.driver.get(self.search_url)
        except Exception:
            log.error('driver unavailable')
            return list()
        page_source = self._get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')
        studios: ResultSet = soup. \
            find_all(name='div', attrs={"class": "content__one-item"})
        for studio in studios:
            try:
                data = self._get_studio_data(studio)
                if self._is_studio_match(data.price, data.footage):
                    self.result.add((data.name, data.link))
            except Exception:
                continue
        log.info(f'matched studios count: {len(self.result)}')
        return list(self.result)

    def _get_search_url(self) -> str:
        url = self.base_url + '/moscow'
        if self.requirements.cyclorama and self.requirements.windows:
            url += '?filter_values[]=38&filter_values[]=3'
        elif self.requirements.cyclorama and not self.requirements.windows:
            url += '/filter/osnashhenie-ciklorama'
        elif not self.requirements.cyclorama and self.requirements.windows:
            url += \
                '/filter/vozmozhnosti_pomeshcheniya_fotostudiy-estestvenniy_dnevnoy_svet'

        log.info(f'search url: {url}')
        return url

    def _wait(self, condition: Callable, locator: str):
        wait = WebDriverWait(self.driver, self.TIMEOUT)
        return wait.until(
            condition(
                ('id', locator)
            )
        )

    def _click_show_more(self, show_more):
        elem_id = "loadButton"
        element = self.driver.find_element_by_id(elem_id)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self._wait(ec.element_to_be_clickable, elem_id)
        self._wait(ec.visibility_of_element_located, elem_id)
        show_more.click()

    def _is_studio_match(self, price: int, footage: int) -> bool:
        if (self.requirements.price_from <= price <= self.requirements.price_to) \
                and (
                self.requirements.footage_from <= footage <= self.requirements.footage_to
        ):
            return True
        return False

    def _get_studio_data(self, studio: Tag) -> StudioData:
        price_element = studio. \
            find(name='div', attrs={'class': "item-content__price"}).text
        price = int(''.join([i for i in price_element if i.isdigit()]))

        link_element = studio. \
            find(name='a', attrs={'class': "item-content__link link-top"})
        link = self.base_url + link_element.attrs['href']

        footage = int(
            studio.find(
                name='div', attrs={'class': "item-content__sizes"}
            ).find(
                name='span', attrs={'class': "item-content__value"}
            ).contents[0].rstrip('м ').rstrip('м2 ')
        )

        name = studio.find(
            name='div', attrs={'class': "item-content__name-studios"}
        ).text.strip()

        return StudioData(price=price, footage=footage, name=name, link=link)

    def _get_page_source(self) -> str:
        show_more = self.driver.find_element_by_xpath("//*[text()='Показать ещё']")
        show_more_click_count = 0
        page_source = None

        while True:
            if show_more_click_count >= MAX_CLICK_SHOW_MORE:
                break
            show_more_click_count += 1
            log.info(
                f"""'show_more' click count: {
                show_more_click_count}, current url: {self.driver.current_url}""",
            )
            try:
                if self.driver.current_url == self.search_url:
                    page_source = self.driver.page_source
                self._click_show_more(show_more)
            except Exception:
                log.warning('stop click show_more')
                break

        return page_source


async def photoplacepro_fabric(user_result: UserInputResult) -> List[Tuple[str]]:
    return PhotoPlaceProController(user_result).find_studios()
