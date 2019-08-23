from aiovk import TokenSession, API
from random import randint
import asyncio

from orm.orm import init_orm
import notifier.notifications as nf


class Notifier:
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        self._session = TokenSession(access_token=token)
        self._api = API(self._session)
        asyncio.get_event_loop().run_until_complete(init_orm(pg_user, pg_password, pg_database, pg_host))

    async def run(self):
        coros = [
            nf.girl_notification(self.write_msg),
            nf.absent_notification(self.write_msg),
        ]

        await asyncio.gather(*coros)

    async def write_msg(self, response_id: int, response: str):
        await self._api('messages.send', peer_id=response_id, message=response, random_id=str(randint(0, 2147483647)))
