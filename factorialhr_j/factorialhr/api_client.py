import requests
from typing import Optional


class ApiError(Exception):
    def __init__(self, status_code: int, message: str, details: Optional[str] = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(self.message)


BASE_URL = "https://api.factorialhr.com"


def get_error_message(response: requests.Response) -> str:
    try:
        error_data = response.json()
        if "errors" in error_data:
            errors = error_data["errors"]
            if isinstance(errors, dict):
                for field, msgs in errors.items():
                    if isinstance(msgs, list):
                        return f"{field}: {', '.join(msgs)}"
                    return f"{field}: {msgs}"
            elif isinstance(errors, list):
                return ", ".join(str(e) for e in errors)
        if "error" in error_data:
            return error_data["error"]
        if "message" in error_data:
            return error_data["message"]
    except Exception:
        pass
    return response.text or response.reason


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        from ..config import get_cookie
        self.cookie = get_cookie()
        self.session.headers.update({"Cookie": self.cookie})

    def _handle_error(self, response: requests.Response):
        if response.status_code == 401:
            raise ApiError(401, "No autorizado. La cookie de sesion ha expirado o es incorrecta.")
        if response.status_code == 422:
            details = get_error_message(response)
            raise ApiError(422, f"Error de validacion (422)", details)
        response.raise_for_status()

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        url = f"{BASE_URL}{path}"
        response = self.session.get(url, params=params)
        self._handle_error(response)
        return response.json()

    def post(self, path: str, json: dict) -> dict:
        url = f"{BASE_URL}{path}"
        response = self.session.post(url, json=json)
        self._handle_error(response)
        return response.json()

    def put(self, path: str, json: dict) -> dict:
        url = f"{BASE_URL}{path}"
        response = self.session.put(url, json=json)
        self._handle_error(response)
        return response.json()

    def delete(self, path: str) -> dict:
        url = f"{BASE_URL}{path}"
        response = self.session.delete(url)
        self._handle_error(response)
        return response.json()