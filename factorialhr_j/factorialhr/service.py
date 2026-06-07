from typing import List
from datetime import datetime

from ..models import CalendarDay, EstimatedTime, WorkedDay, Shift
from .api_client import ApiClient


class FactorialService:
    def __init__(self):
        self.client = ApiClient()

    def get_calendar(self, start_on: str, end_on: str, employee_id: int) -> List[CalendarDay]:
        path = "/attendance/calendar"
        params = {"start_on": start_on, "end_on": end_on, "id": employee_id}
        data = self.client.get(path, params)
        return [CalendarDay.from_api(item) for item in data]

    def get_estimated_times(self, start_on: str, end_on: str, employee_id: int) -> List[EstimatedTime]:
        path = "/api/2026-04-01/resources/attendance/estimated_times"
        params = {
            "employee_ids[]": employee_id,
            "start_on": start_on,
            "end_on": end_on
        }
        data = self.client.get(path, params)
        return [EstimatedTime.from_api(item) for item in data.get("data", [])]

    def get_worked_times(self, start_on: str, end_on: str, employee_id: int) -> List[WorkedDay]:
        path = "/api/2026-04-01/resources/attendance/worked_times"
        params = {
            "employee_ids[]": employee_id,
            "start_on": start_on,
            "end_on": end_on,
            "include_time_range_category": "true",
            "include_non_attendable_employees": "true"
        }
        data = self.client.get(path, params)
        return [WorkedDay.from_api(item) for item in data.get("data", [])]

    def get_shifts(self, start_on: str, end_on: str, employee_id: int) -> List[Shift]:
        path = "/api/2026-04-01/resources/attendance/shifts"
        params = {
            "employee_ids[]": employee_id,
            "start_on": start_on,
            "end_on": end_on
        }
        data = self.client.get(path, params)
        return [Shift.from_api(item) for item in data.get("data", [])]

    def create_shift(self, employee_id: int, date: str, clock_in: str, clock_out: str) -> Shift:
        path = "/api/2026-04-01/resources/attendance/shifts"
        json_data = {
            "employee_id": employee_id,
            "date": date,
            "clock_in": clock_in,
            "clock_out": clock_out
        }
        data = self.client.post(path, json_data)
        return Shift.from_api(data)

    def update_shift(self, shift_id: int, clock_in: str, clock_out: str) -> Shift:
        path = f"/api/2026-04-01/resources/attendance/shifts/{shift_id}"
        json_data = {
            "id": shift_id,
            "clock_in": clock_in,
            "clock_out": clock_out
        }
        data = self.client.put(path, json_data)
        return Shift.from_api(data)

    def delete_shift(self, shift_id: int) -> Shift:
        path = f"/api/2026-04-01/resources/attendance/shifts/{shift_id}"
        data = self.client.delete(path)
        return Shift.from_api(data)