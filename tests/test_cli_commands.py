import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from factorialhr_j.cli import cli
from factorialhr_j.models import Shift, CalendarDay


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_factorial_service_class():
    with patch("factorialhr_j.cli.FactorialService") as mock:
        yield mock


class TestCalendarioCommand:
    def test_calendario_success(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service
        mock_service.get_calendar.return_value = [CalendarDay("2026-06-02", 1, True, False)]
        mock_service.get_estimated_times.return_value = []
        mock_service.get_shifts.return_value = []

        result = runner.invoke(cli, [
            "calendario",
            "--fechainicio", "01/06/2026",
            "--fechafin", "02/06/2026"
        ])

        assert result.exit_code == 0
        assert "Dias desde" in result.output

    def test_calendario_invalid_date(self, runner):
        result = runner.invoke(cli, [
            "calendario",
            "--fechainicio", "02-06-2026",
            "--fechafin", "02/06/2026"
        ])

        assert result.exit_code != 0
        assert "Formato invalido" in result.output

    def test_calendario_start_after_end(self, runner):
        result = runner.invoke(cli, [
            "calendario",
            "--fechainicio", "02/06/2026",
            "--fechafin", "01/06/2026"
        ])

        assert result.exit_code != 0
        assert "anterior" in result.output


class TestImputarCommand:
    def test_imputar_single_success(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service

        mock_shift = Shift(499186575, 12345, "2026-06-02", "2026-06-02T08:00:00", "2026-06-02T15:00:00", True, 420)
        mock_service.create_shift.return_value = mock_shift

        result = runner.invoke(cli, [
            "imputar",
            "--fecha", "02/06/2026",
            "--inicio", "08:00",
            "--fin", "15:00"
        ])

        assert result.exit_code == 0
        assert "creadas: 1" in result.output

    def test_imputar_multiple_success(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service

        mock_shift1 = Shift(1, 12345, "2026-06-02", "2026-06-02T08:00:00", "2026-06-02T15:00:00", True, 420)
        mock_shift2 = Shift(2, 12345, "2026-06-02", "2026-06-02T16:00:00", "2026-06-02T17:30:00", True, 90)
        mock_service.create_shift.side_effect = [mock_shift1, mock_shift2]

        result = runner.invoke(cli, [
            "imputar",
            "--fecha", "02/06/2026",
            "--inicio", "08:00,16:00",
            "--fin", "15:00,17:30"
        ])

        assert result.exit_code == 0
        assert "creadas: 2" in result.output

    def test_imputar_invalid_time(self, runner):
        result = runner.invoke(cli, [
            "imputar",
            "--fecha", "02/06/2026",
            "--inicio", "25:00",
            "--fin", "15:00"
        ])

        assert result.exit_code != 0
        assert "Formato invalido" in result.output

    def test_imputar_fin_before_inicio(self, runner):
        result = runner.invoke(cli, [
            "imputar",
            "--fecha", "02/06/2026",
            "--inicio", "15:00",
            "--fin", "08:00"
        ])

        assert result.exit_code != 0
        assert "anterior" in result.output

    def test_imputar_mismatched_counts(self, runner):
        result = runner.invoke(cli, [
            "imputar",
            "--fecha", "02/06/2026",
            "--inicio", "08:00,16:00",
            "--fin", "15:00"
        ])

        assert result.exit_code != 0
        assert "no coincide" in result.output

    def test_imputar_range_missing_matriz(self, runner):
        result = runner.invoke(cli, [
            "imputar",
            "--rango", "01/06/2026-02/06/2026"
        ])

        assert result.exit_code != 0
        assert "es necesario" in result.output

    def test_imputar_api_error(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service

        from factorialhr_j.factorialhr.api_client import ApiError
        mock_service.create_shift.side_effect = ApiError(422, "Error", "se solapa")

        result = runner.invoke(cli, [
            "imputar",
            "--fecha", "02/06/2026",
            "--inicio", "08:00",
            "--fin", "15:00"
        ])

        assert result.exit_code == 0
        assert "fallidas: 1" in result.output


class TestActualizarImputacionCommand:
    def test_actualizar_success(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service

        mock_shift = Shift(499186575, 12345, "2026-06-02", "2026-06-02T09:00:00", "2026-06-02T16:00:00", True, 420)
        mock_service.get_shifts.return_value = [mock_shift]
        mock_service.update_shift.return_value = mock_shift

        result = runner.invoke(cli, [
            "actualizar-imputacion",
            "--idshift", "499186575",
            "--inicio", "09:00",
            "--fin", "16:00"
        ])

        assert result.exit_code == 0
        assert "actualizada OK" in result.output

    def test_actualizar_invalid_time(self, runner):
        result = runner.invoke(cli, [
            "actualizar-imputacion",
            "--idshift", "123",
            "--inicio", "25:00",
            "--fin", "16:00"
        ])

        assert result.exit_code != 0


class TestBorrarImputacionCommand:
    def test_borrar_by_id_success(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service

        mock_shift = Shift(499186575, 12345, "2026-06-02", "2026-06-02T08:00:00", "2026-06-02T15:00:00", True, 420)
        mock_service.delete_shift.return_value = mock_shift

        result = runner.invoke(cli, [
            "borrar-imputacion",
            "--idshift", "499186575"
        ])

        assert result.exit_code == 0
        assert "eliminadas: 1" in result.output

    def test_borrar_by_fecha_success(self, runner, mock_factorial_service_class):
        mock_service = MagicMock()
        mock_factorial_service_class.return_value = mock_service

        mock_shifts = [
            Shift(1, 12345, "2026-06-02", "2026-06-02T08:00:00", "2026-06-02T15:00:00", True, 420),
            Shift(2, 12345, "2026-06-02", "2026-06-02T16:00:00", "2026-06-02T17:30:00", True, 90),
        ]
        mock_service.get_shifts.return_value = mock_shifts
        mock_service.delete_shift.side_effect = mock_shifts

        result = runner.invoke(cli, [
            "borrar-imputacion",
            "--fecha", "02/06/2026"
        ])

        assert result.exit_code == 0
        assert mock_service.delete_shift.call_count == 2

    def test_borrar_both_params_error(self, runner):
        result = runner.invoke(cli, [
            "borrar-imputacion",
            "--idshift", "123",
            "--fecha", "02/06/2026"
        ])

        assert result.exit_code != 0
        assert "a la vez" in result.output

    def test_borrar_no_params_error(self, runner):
        result = runner.invoke(cli, [
            "borrar-imputacion"
        ])

        assert result.exit_code != 0
        assert "Use --idshift" in result.output