import click
from datetime import datetime
from typing import Tuple, List


DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M"
RANGE_FORMAT = f"{DATE_FORMAT}-{DATE_FORMAT}"


def validate_date(date_str: str, param_name: str = "fecha") -> datetime:
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise click.BadParameter(f"Formato invalido para '{param_name}'. Uso: DD/MM/YYYY (ej: 02/06/2026)")


def validate_time(time_str: str, param_name: str = "hora") -> None:
    try:
        datetime.strptime(time_str, TIME_FORMAT)
    except ValueError:
        raise click.BadParameter(f"Formato invalido para '{param_name}'. Uso: HH:MM (ej: 08:30)")


def validate_times_csv(times_str: str, param_name: str) -> List[str]:
    times = [t.strip() for t in times_str.split(",")]
    for t in times:
        validate_time(t, param_name)
    return times


def validate_range(range_str: str, param_name: str = "rango") -> Tuple[datetime, datetime]:
    if "-" not in range_str:
        raise click.BadParameter(f"Formato invalido para '{param_name}'. Uso: DD/MM/YYYY-DD/MM/YYYY (ej: 01/06/2026-02/06/2026)")

    parts = range_str.split("-", 1)
    if len(parts) != 2:
        raise click.BadParameter(f"Formato invalido para '{param_name}'. Uso: DD/MM/YYYY-DD/MM/YYYY (ej: 01/06/2026-02/06/2026)")

    start_str, end_str = parts[0].strip(), parts[1].strip()

    try:
        start_dt = datetime.strptime(start_str, DATE_FORMAT)
    except ValueError:
        raise click.BadParameter(f"Formato invalido para fecha inicio en '{param_name}'. Uso: DD/MM/YYYY (ej: 02/06/2026)")

    try:
        end_dt = datetime.strptime(end_str, DATE_FORMAT)
    except ValueError:
        raise click.BadParameter(f"Formato invalido para fecha fin en '{param_name}'. Uso: DD/MM/YYYY (ej: 02/06/2026)")

    if start_dt > end_dt:
        raise click.BadParameter(f"La fecha inicio debe ser anterior o igual a la fecha fin en '{param_name}'")

    return start_dt, end_dt


def validate_time_range(start_time: str, end_time: str, param_start: str = "inicio", param_end: str = "fin") -> None:
    start_dt = datetime.strptime(start_time, TIME_FORMAT)
    end_dt = datetime.strptime(end_time, TIME_FORMAT)
    if start_dt >= end_dt:
        raise click.BadParameter(f"La hora '{param_start}' debe ser anterior a la hora '{param_end}'")