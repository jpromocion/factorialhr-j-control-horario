from dataclasses import dataclass
from typing import List


@dataclass
class CalendarDay:
    date: str
    day: int
    is_laborable: bool
    is_leave: bool

    @staticmethod
    def from_api(data: dict) -> "CalendarDay":
        return CalendarDay(
            date=data["date"],
            day=data["day"],
            is_laborable=data["is_laborable"],
            is_leave=data["is_leave"]
        )