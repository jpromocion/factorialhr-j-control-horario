import pytest
from unittest.mock import MagicMock, patch

from factorialhr_j.models import Shift, CalendarDay


@pytest.fixture
def mock_employee_id():
    return 12345


@pytest.fixture
def sample_shift():
    return Shift(
        id=499186575,
        date="2026-06-02",
        clock_in="2026-06-02T08:00:00",
        clock_out="2026-06-02T15:00:00",
        workable=True,
        minutes=420
    )


@pytest.fixture
def sample_calendar_day():
    return CalendarDay(
        date="2026-06-02",
        day=1,
        is_laborable=True,
        is_leave=False
    )


@pytest.fixture
def mock_factorial_service():
    with patch("factorialhr_j.cli.FactorialService") as mock:
        yield mock


@pytest.fixture
def mock_click_echo():
    with patch("click.echo") as mock:
        yield mock