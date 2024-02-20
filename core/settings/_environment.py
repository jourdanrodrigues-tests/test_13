import json
import os

from dotenv import load_dotenv


def bool_env(key, default: bool) -> bool:
    value = os.getenv(key)
    return json.loads(value) if value in ["true", "false"] else default


def get_host_env(key: str, default: list[str]) -> list[str]:
    value = os.getenv(key)
    if value:
        return value.split(",")
    return default


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")

PRODUCTION = bool_env("PRODUCTION", False)
DEBUG = bool_env("DEBUG", not PRODUCTION)

ALLOWED_HOSTS = get_host_env("ALLOWED_HOSTS", [] if PRODUCTION else ["*"])
ALLOWED_CLIENTS = get_host_env("ALLOWED_CLIENTS", ALLOWED_HOSTS)
