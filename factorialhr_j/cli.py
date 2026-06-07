import click
import json
from typing import Dict, List, Optional, Tuple

from .factorialhr import FactorialService
from .factorialhr.api_client import ApiError
from .config import get_employee_id
from .validators import validate_date, validate_range, validate_time, validate_times_csv, validate_time_range
from .utils import (
    format_date,
    format_minutes,
    format_time,
    get_day_letter,
    output_error,
    output_warning,
    output_completion,
    output_shifts_results,
    output_single_shift,
    output_calendar,
)


@click.group()
def cli():
    pass


@cli.command("calendario")
@click.option("--fechainicio", required=True, help="Fecha inicio (DD/MM/YYYY)")
@click.option("--fechafin", required=True, help="Fecha fin (DD/MM/YYYY)")
def calendario(fechainicio: str, fechafin: str):
    try:
        employee_id = get_employee_id()
        start_dt = validate_date(fechainicio, "--fechainicio")
        end_dt = validate_date(fechafin, "--fechafin")
        if start_dt > end_dt:
            raise click.BadParameter("La fecha de inicio debe ser anterior o igual a la fecha fin")
        start_on = start_dt.strftime("%Y-%m-%d")
        end_on = end_dt.strftime("%Y-%m-%d")

        service = FactorialService()

        calendar_days = service.get_calendar(start_on, end_on, employee_id)
        estimated_times = service.get_estimated_times(start_on, end_on, employee_id)
        worked_days = service.get_worked_times(start_on, end_on, employee_id)
        shifts = service.get_shifts(start_on, end_on, employee_id)

        estimated_dict: Dict[str, int] = {e.date: int(e.minutes) for e in estimated_times}
        shifts_by_date: Dict[str, List] = {}
        for shift in shifts:
            if shift.workable:
                if shift.date not in shifts_by_date:
                    shifts_by_date[shift.date] = []
                shifts_by_date[shift.date].append(shift)

        output_calendar(calendar_days, shifts_by_date, estimated_dict, fechainicio, fechafin)
    except ApiError as e:
        output_error(f"Error {e.status_code}: {e.message}", e.details)
        raise SystemExit(1)


@cli.command("imputar")
@click.option("--fecha", help="Fecha (DD/MM/YYYY)")
@click.option("--inicio", help="Hora inicio (HH:MM), puede usar commas para multiples")
@click.option("--fin", help="Hora fin (HH:MM), puede usar commas para multiples")
@click.option("--rango", help="Rango de fechas (DD/MM/YYYY-DD/MM/YYYY)")
@click.option("--matriz-modelo", help="Matriz modelo JSON por tipo de dia de la semana")
def imputar(fecha: Optional[str], inicio: Optional[str], fin: Optional[str],
             rango: Optional[str], matriz_modelo: Optional[str]):
    try:
        employee_id = get_employee_id()
        service = FactorialService()
        results: Dict[str, Tuple[List, List]] = {}

        if rango or matriz_modelo:
            if not rango or not matriz_modelo:
                output_error("Cuando se usa 'rango' es necesario 'matriz-modelo' y vicecersa")
                raise SystemExit(1)

            start_dt, end_dt = validate_range(rango, "--rango")
            start_on = start_dt.strftime("%Y-%m-%d")
            end_on = end_dt.strftime("%Y-%m-%d")
            matriz = json.loads(matriz_modelo)
            matriz_by_day = {entry["dia"]: entry["imputaciones"] for entry in matriz}

            calendar_days = service.get_calendar(start_on, end_on, employee_id)

            for cal_day in calendar_days:
                if not cal_day.is_laborable or cal_day.is_leave:
                    continue

                day_letter = get_day_letter(cal_day.date)
                if day_letter not in matriz_by_day:
                    continue

                imputaciones = matriz_by_day[day_letter]
                if not imputaciones:
                    continue

                results[cal_day.date] = ([], [])

                for imp in imputaciones:
                    validate_time(imp["inicio"], "--matriz-modelo inicio")
                    validate_time(imp["fin"], "--matriz-modelo fin")
                    validate_time_range(imp["inicio"], imp["fin"], "--matriz-modelo inicio", "--matriz-modelo fin")
                    clock_in = f"{cal_day.date}T{imp['inicio']}:00"
                    clock_out = f"{cal_day.date}T{imp['fin']}:00"
                    try:
                        shift = service.create_shift(employee_id, cal_day.date, clock_in, clock_out)
                        results[cal_day.date][0].append(shift)
                    except ApiError as e:
                        results[cal_day.date][1].append(f"Error {e.status_code}: {e.message}" + (f"\n        Detalle: {e.details}" if e.details else ""))

        else:
            if not fecha or not inicio or not fin:
                output_error("Faltan parametros. Use --fecha/--inicio/--fin o --rango/--matriz-modelo")
                raise SystemExit(1)

            date_dt = validate_date(fecha, "--fecha")
            date_api = date_dt.strftime("%Y-%m-%d")

            inicio_list = validate_times_csv(inicio, "--inicio")
            fin_list = validate_times_csv(fin, "--fin")

            if len(inicio_list) != len(fin_list):
                output_error(f"El numero de elementos en inicio ({len(inicio_list)}) y fin ({len(fin_list)}) no coincide")
                raise SystemExit(1)

            for ini, fin_time in zip(inicio_list, fin_list):
                validate_time_range(ini, fin_time, "--inicio", "--fin")

            results[date_api] = ([], [])

            for ini, fin_time in zip(inicio_list, fin_list):
                clock_in = f"{date_api}T{ini}:00"
                clock_out = f"{date_api}T{fin_time}:00"
                try:
                    shift = service.create_shift(employee_id, date_api, clock_in, clock_out)
                    results[date_api][0].append(shift)
                except ApiError as e:
                    results[date_api][1].append(f"Error {e.status_code}: {e.message}" + (f"\n        Detalle: {e.details}" if e.details else ""))

        if not results or all(len(shifts) == 0 and len(errors) == 0 for shifts, errors in results.values()):
            output_warning("No se ha creado ninguna imputacion")
        else:
            output_shifts_results(results, "creadas")

    except ApiError as e:
        output_error(f"Error {e.status_code}: {e.message}", e.details)
        raise SystemExit(1)


@cli.command("actualizar-imputacion")
@click.option("--idshift", required=True, type=int, help="ID del shift")
@click.option("--inicio", required=True, help="Hora inicio (HH:MM)")
@click.option("--fin", required=True, help="Hora fin (HH:MM)")
def actualizar_imputacion(idshift: int, inicio: str, fin: str):
    try:
        validate_time(inicio, "--inicio")
        validate_time(fin, "--fin")
        validate_time_range(inicio, fin, "--inicio", "--fin")

        service = FactorialService()

        shifts = service.get_shifts("2000-01-01", "2099-12-31", get_employee_id())
        shift_find = next((s for s in shifts if s.id == idshift), None)

        date_api = shift_find.date if shift_find else ""

        clock_in = f"{date_api}T{inicio}:00" if date_api else f"2000-01-01T{inicio}:00"
        clock_out = f"{date_api}T{fin}:00" if date_api else f"2000-01-01T{fin}:00"

        shift = service.update_shift(idshift, clock_in, clock_out)

        output_single_shift(shift, "actualizada")
    except ApiError as e:
        output_error(f"Error {e.status_code}: {e.message}", e.details)
        raise SystemExit(1)


@cli.command("borrar-imputacion")
@click.option("--idshift", type=int, help="ID del shift")
@click.option("--fecha", help="Fecha (DD/MM/YYYY) - elimina todas las imputaciones del dia")
def borrar_imputacion(idshift: Optional[int], fecha: Optional[str]):
    try:
        service = FactorialService()
        employee_id = get_employee_id()
        results: Dict[str, Tuple[List, List]] = {}

        if fecha:
            if idshift is not None:
                output_error("No se puede usar --idshift y --fecha a la vez")
                raise SystemExit(1)

            date_dt = validate_date(fecha, "--fecha")
            date_api = date_dt.strftime("%Y-%m-%d")

            shifts = service.get_shifts(date_api, date_api, employee_id)
            results[date_api] = ([], [])

            for shift in shifts:
                try:
                    deleted = service.delete_shift(shift.id)
                    results[date_api][0].append(deleted)
                except ApiError as e:
                    results[date_api][1].append(f"Error {e.status_code}: {e.message}" + (f"\n        Detalle: {e.details}" if e.details else ""))

        elif idshift is not None:
            shift = service.delete_shift(idshift)
            results[shift.date] = ([shift], [])

        else:
            output_error("Use --idshift o --fecha")
            raise SystemExit(1)

        if not results or all(len(shifts) == 0 and len(errors) == 0 for shifts, errors in results.values()):
            output_warning("No se ha eliminado ninguna imputacion")
        else:
            output_shifts_results(results, "eliminadas")

    except ApiError as e:
        output_error(f"Error {e.status_code}: {e.message}", e.details)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()