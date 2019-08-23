from aiovk import TokenSession, API
from random import randint
import asyncio

from orm.orm import init_orm
import crawler.crawler_funcs as cf


class Crawler:
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        self._session = TokenSession(access_token=token)
        self._api = API(self._session)
        asyncio.get_event_loop().run_until_complete(init_orm(pg_user, pg_password, pg_database, pg_host))

    async def run(self):
        coros = [
            # cf.load_conversations(self._api),
            cf.update_names(self._api),
        ]

        await asyncio.gather(*coros)
