import asyncio
from os import environ

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'


def get_env_var(name: str, default=None):
    try:
        return environ[name]
    except KeyError:
        return default

