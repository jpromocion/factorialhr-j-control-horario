import pytest
import click
from factorialhr_j.validators import (
    validate_date,
    validate_time,
    validate_times_csv,
    validate_range,
    validate_time_range,
)


class TestValidateDate:
    def test_valid_date_returns_datetime(self):
        result = validate_date("02/06/2026", "--fecha")
        assert result.year == 2026
        assert result.month == 6
        assert result.day == 2

    def test_invalid_date_raises_bad_parameter(self):
        with pytest.raises(click.BadParameter):
            validate_date("02-06-2026", "--fecha")

    def test_invalid_format_raises_bad_parameter(self):
        with pytest.raises(click.BadParameter):
            validate_date("abc", "--fecha")


class TestValidateTime:
    def test_valid_time_passes(self):
        validate_time("08:00", "--inicio")

    def test_invalid_time_raises_bad_parameter(self):
        with pytest.raises(click.BadParameter):
            validate_time("25:00", "--inicio")

    def test_invalid_format_raises_bad_parameter(self):
        with pytest.raises(click.BadParameter):
            validate_time("8-00", "--inicio")


class TestValidateTimesCsv:
    def test_valid_csv_passes(self):
        result = validate_times_csv("08:00,16:00", "--inicio")
        assert result == ["08:00", "16:00"]

    def test_csv_with_spaces_passes(self):
        result = validate_times_csv("08:00, 16:00", "--inicio")
        assert result == ["08:00", "16:00"]

    def test_invalid_time_in_csv_raises(self):
        with pytest.raises(click.BadParameter):
            validate_times_csv("08:00,25:00", "--inicio")


class TestValidateRange:
    def test_valid_range_returns_tuple(self):
        start, end = validate_range("01/06/2026-02/06/2026", "--rango")
        assert start.strftime("%Y-%m-%d") == "2026-06-01"
        assert end.strftime("%Y-%m-%d") == "2026-06-02"

    def test_start_after_end_raises(self):
        with pytest.raises(click.BadParameter):
            validate_range("02/06/2026-01/06/2026", "--rango")

    def test_invalid_format_raises(self):
        with pytest.raises(click.BadParameter):
            validate_range("01/06/2026", "--rango")


class TestValidateTimeRange:
    def test_start_before_end_passes(self):
        validate_time_range("08:00", "15:00", "--inicio", "--fin")

    def test_start_equals_end_raises(self):
        with pytest.raises(click.BadParameter):
            validate_time_range("15:00", "15:00", "--inicio", "--fin")

    def test_start_after_end_raises(self):
        with pytest.raises(click.BadParameter):
            validate_time_range("16:00", "08:00", "--inicio", "--fin")