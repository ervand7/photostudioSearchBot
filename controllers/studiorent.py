from asyncio import gather
from logging import getLogger
from typing import List

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from more_itertools import chunked

from controllers.base import BaseController
from views.base import UserInputResult

log = getLogger(__name__)


class StudioRentController(BaseController):
    """ https://www.studiorent.ru """

    def __init__(self, requirements: UserInputResult):
        super().__init__()
        self.requirements = self.check_requirements(requirements)
        self.base_url = 'https://www.studiorent.ru'
        self.search_url = self._get_search_url()
        self.result = set()

    def find_studios(self) -> List[str]:
        text: str = requests.get(self.search_url).text
        soup = BeautifulSoup(text, 'html.parser')
        studios: ResultSet = soup.find_all(name='article', attrs={"class": "s spo"})
        studios += soup.find_all(name='article', attrs={"class": "s"})
        urls = set()
        for studio in studios:  # type: Tag
            href: str = studio.find(name='a', attrs={'class': "counters-click"}).attrs['href']
            url = self.base_url + href
            urls.add(url)

        log.info(f'matched studios count: {len(urls)}')
        return list(urls)

    def _get_search_url(self) -> str:
        url = 'https://www.studiorent.ru/studios/?city=33'
        if self.requirements.price_from:
            url += f'&price_start={self.requirements.price_from}'
        if self.requirements.price_to:
            url += f'&price_end={self.requirements.price_to}'
        if self.requirements.cyclorama:
            url += '&cyclorama=on'
        if self.requirements.windows:
            url += '&windows=on'
        if self.requirements.footage_from:
            url += f'&area_start={self.requirements.footage_from}'
        if self.requirements.footage_to:
            url += f'&area_end={self.requirements.footage_to}'

        log.info(f'search url: {url}')
        return url

    async def event_loop(self, urls: List[str]):
        async with ClientSession() as async_session:
            tasks = [self._studio_request(async_session, url) for url in urls]
            for chunk in chunked(tasks, 50):
                await gather(*chunk)

    async def _studio_request(self, async_session: ClientSession, url: str) -> None:
        resp = await async_session.get(url)
        page_source = await resp.text()
        soup = BeautifulSoup(page_source, 'html.parser')
        studio_name: str = \
            soup.find(name='span', attrs={'class': "text-muted"}).contents[0]
        metro_station = ''
        try:
            metro_station = \
                soup.find(name='i', attrs={'class': "fa-li fa fa-subway"}).next
        except Exception:
            log.warning(f'no metro for {studio_name}')
        metro_station = f'(м. {metro_station.strip()}) ' if metro_station else metro_station

        log.info(f'{studio_name} {url}')
        self.result.add((metro_station + studio_name, url))


async def studiorent_fabric(user_result: UserInputResult) -> List[str]:
    page_elem_count = 50
    controller = StudioRentController(user_result)
    studios = []
    counter = 1
    while True:
        try:
            links = controller.find_studios()
            await controller.event_loop(links)
            studios += list(controller.result)
            if len(links) == page_elem_count:
                counter += 1
                controller.search_url += f'&page={counter}'
            else:
                break
        except Exception:
            log.info('studiorent_fabric: stop pagination')
    return list(set(studios))
