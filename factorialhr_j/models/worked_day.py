from dataclasses import dataclass
from typing import List


@dataclass
class WorkedTimeBlock:
    minutes: int
    workable: bool

    @staticmethod
    def from_api(data: dict) -> "WorkedTimeBlock":
        return WorkedTimeBlock(
            minutes=data["minutes"],
            workable=data["workable"]
        )


@dataclass
class WorkedDay:
    date: str
    minutes: int
    worked_time_blocks: List[WorkedTimeBlock]

    @staticmethod
    def from_api(data: dict) -> "WorkedDay":
        blocks = [WorkedTimeBlock.from_api(b) for b in data.get("worked_time_blocks", [])]
        return WorkedDay(
            date=data["date"],
            minutes=data["minutes"],
            worked_time_blocks=blocks
        )