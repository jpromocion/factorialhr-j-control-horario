import os
from pathlib import Path
from typing import Optional
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_BASE_PATH = BASE_DIR / "config" / "config.base.yaml"
CONFIG_USER_PATH = BASE_DIR / "config" / "config.yaml"


def load_config() -> dict:
    config_data = {}

    if CONFIG_USER_PATH.exists():
        with open(CONFIG_USER_PATH, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            config_data.update(user_config)

    if CONFIG_BASE_PATH.exists():
        with open(CONFIG_BASE_PATH, "r", encoding="utf-8") as f:
            base_config = yaml.safe_load(f) or {}
            for key, value in base_config.items():
                if key not in config_data:
                    config_data[key] = value

    return config_data


def get_employee_id() -> int:
    config = load_config()
    return int(config.get("id_empleado", 0))


def get_cookie() -> str:
    config = load_config()
    return config.get("cookie_sesion", "")