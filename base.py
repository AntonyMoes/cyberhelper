from aiovk import TokenSession, API
from random import randint
import asyncio
from time import time

from orm.orm import init_orm
from orm.models import Conversation


class BaseBot:
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        self._session = TokenSession(access_token=token)
        self._session.API_VERSION = '5.101'
        self._api = API(self._session)
        asyncio.get_event_loop().run_until_complete(init_orm(pg_user, pg_password, pg_database, pg_host))

    @staticmethod
    async def _run(coros):
        await asyncio.gather(*coros)

    async def write_msg(self, person_id: int, response: str, chat_id: int = -1, reply_id: int = -1):
        if chat_id == -1:
            chat_id = person_id

        params = {
            'peer_id': chat_id,
            'message': response,
            'random_id': str(randint(0, 2147483647)),
        }

        if reply_id != -1:
            params['reply_to'] = reply_id

        await self._api('messages.send', **params)
        await Conversation.objects.filter(id=person_id).update(last_ts=int(time()))
