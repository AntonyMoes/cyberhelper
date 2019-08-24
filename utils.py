import asyncio
from os import environ

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


def get_env_var(name: str, default=None):
    try:
        return environ[name]
    except KeyError:
        return default

