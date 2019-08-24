from random import randint
from time import time

from bot.quotes import get_quote
from bot.ads import get_ad
from generator import Generator
from orm.models import Conversation
from utils import sync


class Processor:
    def __init__(self):
        self._gen = Generator('trained_data/cyber_weights')

    def process(self, message: str, response_id: int) -> str:
        self._update_conversation(response_id)
        is_ad = randint(1, 15) == 1
        if is_ad:
            return get_ad()

        if message.find('цитата') != -1:
            return get_quote()
        else:
            return self._gen.generate(seed=message, size=randint(10, 80))

    @staticmethod
    @sync
    async def _update_conversation(response_id: int):
        ts = int(time())
        try:
            conversation = await Conversation.objects.filter(id=response_id).get_one()
            conversation.last_ts = ts
            await conversation.save()
        except Conversation.DoesNotExist:
            await Conversation.objects.create(id=response_id, last_ts=ts)
