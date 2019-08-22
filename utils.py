import asyncio
from os import environ


def sync(coro):
    def _helper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(coro(*args, **kwargs))
    return _helper


def get_env_var(name: str, default=None):
    try:
        return environ[name]
    except KeyError:
        return default

