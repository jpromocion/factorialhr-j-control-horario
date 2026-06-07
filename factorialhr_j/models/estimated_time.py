from dataclasses import dataclass


@dataclass
class EstimatedTime:
    date: str
    minutes: float

    @staticmethod
    def from_api(data: dict) -> "EstimatedTime":
        return EstimatedTime(
            date=data["date"],
            minutes=data["minutes"]
        )