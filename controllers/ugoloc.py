from logging import getLogger
from time import sleep
from typing import List, Tuple

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from controllers.base import BaseController
from views.base import UserInputResult

log = getLogger(__name__)

TIME_LOAD_PAGE = 15


class UgolocController(BaseController):
    """ https://ugoloc.ru/ """

    def __init__(self, requirements):
        super().__init__()
        self.requirements = self.check_requirements(requirements)
        self.search_url = self._get_search_url()
        self.result = set()

    def find_studios(self) -> List[Tuple[str, str]]:
        self.driver.get(self.search_url)
        log.info('waiting for page load...')
        sleep(TIME_LOAD_PAGE)
        text = self.driver.page_source
        soup = BeautifulSoup(text, 'html.parser')
        studios: ResultSet = soup. \
            find_all(name='div', attrs={"class": "location catalog__item"})
        data = set()
        for studio in studios:  # type: Tag
            url: str = studio.find(name='a', attrs={'class': "location__link"}).attrs['href']
            name: str = studio.text.strip()
            log.info(f'matched {(name, url)}')
            data.add((name, url))

        log.info(f'matched studios count: {len(data)}')
        return list(data)

    def _get_search_url(self) -> str:
        price_from = self.requirements.price_from if self.requirements.price_from else 0
        price_to = self.requirements.price_to if self.requirements.price_to else 0
        cyclorama = 'characteristics[0]=4&' if self.requirements.cyclorama else ''
        windows = 'characteristics[1]=5&' if self.requirements.windows else ''
        if self.requirements.footage_to < 50:
            square = 'square[min]=3&square[max]=50&'
        elif self.requirements.footage_from > 50 and self.requirements.footage_to < 100:
            square = 'square[min]=50&square[max]=100&'
        else:
            square = 'square[min]=100&square[max]=20000&'

        url = f"""https://ugoloc.ru/moscow/studios/filter?{cyclorama}{windows}price[min]={
        price_from}&price[max]={price_to}&city_id=1&time=on_hour&{
        square}instant=1&hasPromoCode=0"""

        log.info(f'search url: {url}')
        return url


async def ugoloc_fabric(user_result: UserInputResult) -> List[Tuple[str, str]]:
    return UgolocController(user_result).find_studios()
