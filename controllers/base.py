from abc import ABC, abstractmethod
from dataclasses import asdict
from logging import getLogger
from typing import List, Tuple

from app import driver
from views.base import UserInputResult

log = getLogger(__name__)


class BaseController(ABC):
    def __init__(self):
        self.driver = driver

    @abstractmethod
    def find_studios(self) -> List[Tuple[str]]:
        raise NotImplemented()

    @abstractmethod
    def _get_search_url(self) -> str:
        raise NotImplemented()

    @staticmethod
    def check_requirements(requirements: UserInputResult) \
            -> UserInputResult:
        if requirements.price_from is None:
            requirements.price_from = 500
        if requirements.price_to is None:
            requirements.price_to = 5000
        if requirements.footage_from is None:
            requirements.footage_from = 30
        if requirements.footage_to is None:
            requirements.footage_to = 150

        user_set_params = {k: v for k, v in asdict(requirements).items() if v}
        log.info(f'user set search params: {user_set_params}')
        return requirements
