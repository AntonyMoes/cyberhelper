from random import randint
from time import time

from bot.commands import check_command, process_command, Command
from bot.ads import get_ad
from generator import Generator
from orm.models import Conversation


class Processor:
    def __init__(self):
        self._gen = Generator('trained_data/cyber_weights')

    async def process(self, message: str, person_id: int) -> str:
        await self._update_conversation(person_id)
        message = message.lower().strip()

        command, info = check_command(message)
        if command != Command.Unknown:
            try:
                return await process_command(command, info, person_id)
            except ValueError:
                return f'Неправильные параметры({info}) для команды "{command.value}"'

        is_ad = randint(1, 15) == 1
        if is_ad:
            return get_ad()

        return self._gen.generate(seed=message, size=randint(10, 80))

    @staticmethod
    async def _update_conversation(person_id: int):
        ts = int(time())
        try:
            conversation = await Conversation.objects.filter(id=person_id).get_one()
            conversation.last_ts = ts
            await conversation.save()
        except Conversation.DoesNotExist:
            await Conversation.objects.create(id=person_id, last_ts=ts)
