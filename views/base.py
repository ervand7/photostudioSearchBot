from dataclasses import dataclass
from datetime import datetime, time


@dataclass
class UserInputResult:
    date: datetime = None
    time_start: time = None
    time_end: time = None
    cyclorama: bool = None
    price_from: int = None
    price_to: int = None
    windows: bool = None
    footage_from: int = None
    footage_to: int = None

    def reset(self) -> None:
        for field in self.__dict__:
            setattr(user_result, field, None)


user_result = UserInputResult()
