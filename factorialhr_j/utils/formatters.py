from datetime import datetime

DAY_LETTERS = ["L", "M", "X", "J", "V", "S", "D"]


def format_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%d/%m/%Y")


def format_minutes(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours} horas - {mins} minutos"


def format_time(time_str: str) -> str:
    if "T" in time_str:
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%H:%M")
    return time_str


def get_day_letter(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return DAY_LETTERS[dt.weekday()]