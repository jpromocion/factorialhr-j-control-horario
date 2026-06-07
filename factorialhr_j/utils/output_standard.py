import click
from typing import Dict, List, Tuple, Optional

from .formatters import format_date, format_minutes, format_time


def output_error(message: str, details: Optional[str] = None):
    click.echo(click.style(f"\n❌ {message}", fg="red"), err=True)
    if details:
        click.echo(click.style(f"   Detalle: {details}", fg="yellow"), err=True)


def output_warning(message: str):
    click.echo(click.style(f"⚠️  {message}", fg="yellow"))


def output_completion():
    click.echo(f"\n{click.style('🎯 Proceso completado!', fg='yellow')}")


def output_shifts_results(results: Dict[str, Tuple[List, List]], action_verb: str = "creadas"):
    total_ok = 0
    total_failed = 0

    for date_str, (shifts, errors) in sorted(results.items()):
        click.echo(click.style(f"\n  📆 DIA: {format_date(date_str)}", fg="yellow"))
        click.echo(click.style("  " + "─" * 38, fg="yellow"))

        for error in errors:
            click.echo(click.style(f"    ❌ {error}", fg="red"))

        for idx, shift in enumerate(shifts, 1):
            click.echo(click.style(f"    {idx}️⃣  🕐 {format_time(shift.clock_in)} - {format_time(shift.clock_out)}", fg="cyan"))
            click.echo(f"        ⏱️  {format_minutes(shift.minutes)}")
            click.echo(click.style(f"        🆔 Id shift: {shift.id}", fg="cyan"))

        total_ok += len(shifts)
        total_failed += len(errors)

    if total_ok > 0:
        click.echo(click.style(f"\n✅ Imputaciones {action_verb}: {total_ok}", fg="green"))

    if total_failed > 0:
        click.echo(click.style(f"❌ Imputaciones fallidas: {total_failed}", fg="red"))

    output_completion()


def output_single_shift(shift, action_verb: str = "actualizada"):
    click.echo(click.style(f"✅ Imputacion {action_verb} OK", fg="green"))
    click.echo(f"   📆 Dia: {format_date(shift.date)}")
    click.echo(f"   🆔 Id shift: {shift.id}")
    click.echo(f"   🕐 Hora inicio: {format_time(shift.clock_in)}")
    click.echo(f"   🕑 Hora fin: {format_time(shift.clock_out)}")
    click.echo(click.style(f"   ⏱️  Tiempo: {format_minutes(shift.minutes)}", fg="cyan"))
    output_completion()


def output_calendar(
    calendar_days,
    shifts_by_date: Dict[str, List],
    estimated_dict: Dict[str, int],
    fechainicio: str,
    fechafin: str
):
    click.echo(f"📅 Dias desde {fechainicio} hasta {fechafin}")
    click.echo("─" * 50)

    for cal_day in calendar_days:
        date_display = format_date(cal_day.date)

        click.echo(click.style(f"\n📆 DIA: {date_display}", fg="yellow"))
        click.echo(click.style("─" * 40, fg="yellow"))

        if cal_day.is_laborable:
            click.echo("   ✅ Laborable", nl=False)
        else:
            click.echo(click.style("   ❌ No laborable", fg="red"), nl=False)

        if cal_day.is_leave:
            click.echo("   " + click.style("🔴 Festivo", fg="red"))
        else:
            click.echo("   ⚪ No festivo")

        day_shifts = shifts_by_date.get(cal_day.date, [])
        total_minutes = sum(s.minutes for s in day_shifts)
        expected_minutes = estimated_dict.get(cal_day.date, 0)

        click.echo(click.style(f"   ⏱️  Tiempo estimado: {format_minutes(expected_minutes)}", fg="green"))
        click.echo(click.style(f"   ⏱️  Tiempo imputedo: {format_minutes(total_minutes)}", fg="blue"))

        if cal_day.is_laborable and expected_minutes > 0 and total_minutes != expected_minutes:
            diff = abs(expected_minutes - total_minutes)
            if total_minutes == 0:
                click.echo(click.style(f"   ⚠️  ALERTA: Dia sin imputar. Faltan {format_minutes(diff)}", fg="red"))
            else:
                click.echo(click.style(f"   ⚠️  ALERTA: Tiempo no coincide. Diferencia: {format_minutes(diff)}", fg="red"))

        if day_shifts:
            click.echo("   📋 Desglose:")
            for shift in day_shifts:
                clock_in = format_time(shift.clock_in)
                clock_out = format_time(shift.clock_out)
                click.echo(f"      🕑 {clock_in} - {clock_out} -> {format_minutes(shift.minutes)}  (Id shift: {click.style(str(shift.id), fg='cyan')})")

    output_completion()