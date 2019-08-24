from random import randint
import asyncio
from aiovk.longpoll import BotsLongPoll

from base import BaseBot
from bot.processor import Processor
from bot.events import Event, VkEventType


class Bot(BaseBot):
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        super().__init__(token, pg_user, pg_password, pg_database, pg_host)

        self._longpoll = BotsLongPoll(self._api, mode=[2, 8], group_id=185597155)
        self._pr = Processor()

    async def run(self):
        while True:
            updates = (await self._longpoll.wait())['updates']
            for update in updates:
                event = Event(update)
                print(event, '\n')

                if event.msg_to_me:
                    reply = await self._pr.process(event.text.lower(), event.from_id)

                    if event.to_chat:
                        await self.write_msg(person_id=event.from_id, response=reply, chat_id=event.chat_id)
                    else:
                        await self.write_msg(person_id=event.from_id, response=reply)



