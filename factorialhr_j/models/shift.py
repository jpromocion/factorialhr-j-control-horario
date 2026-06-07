from dataclasses import dataclass


@dataclass
class Shift:
    id: int
    employee_id: int
    date: str
    clock_in: str
    clock_out: str
    workable: bool
    minutes: int

    @staticmethod
    def from_api(data: dict) -> "Shift":
        return Shift(
            id=data["id"],
            employee_id=data["employee_id"],
            date=data["date"],
            clock_in=data["clock_in"],
            clock_out=data["clock_out"],
            workable=data["workable"],
            minutes=data["minutes"]
        )