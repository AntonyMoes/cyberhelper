from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
import asyncio

from bot.processor import Processor
from orm.orm import init_orm


class Bot:
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        self._vk = VkApi(token=token)
        self._longpoll = VkLongPoll(self._vk)
        self._pr = Processor()
        asyncio.get_event_loop().run_until_complete(init_orm(pg_user, pg_password, pg_database, pg_host))

    def run(self):
        for event in self._longpoll.listen():
            # print(event.type)
            if event.type == VkEventType.MESSAGE_NEW:
                # print(event.text)
                if event.to_me:
                    request = event.text.lower()
                    response_id = event.user_id

                    response = self._pr.process(request, response_id)
                    self.write_msg(self._vk, response_id, response)

    @staticmethod
    def write_msg(vk: VkApi, response_id: int, response: str):
        vk.method('messages.send',
                  {'peer_id': response_id, 'message': response, 'random_id': str(randint(0, 2147483647))})

