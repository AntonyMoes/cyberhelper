from random import choice, randint
from time import time
import asyncio

from orm.models import Conversation
from utils import HOUR, DAY

girls = [
    'Надя',
    'Лена',
    'Лена',
    'Алиса',
    'Маша',
    'Даша',
]


async def girl_notification(write):
    while True:
        try:
            conversations = await Conversation.objects.get()
        except Conversation.DoesNotExist:
            await asyncio.sleep(HOUR)
            continue

        conversation = choice(conversations)
        girl = choice(girls)

        if conversation.name is None:
            message = f'Здравствуйте. ' \
                      f'Не могли бы вы узнать, почему {girl} игнорирует меня вконтакте?'
        else:
            message = f'Здравствуйте, {conversation.name}. ' \
                      f'Не могли бы вы узнать, почему {girl} игнорирует меня вконтакте?'

        await write(conversation.id, message)

        await asyncio.sleep(randint(HOUR * 8, DAY))


async def absent_notification(write):
    while True:
        try:
            conversations = await Conversation.objects.get()
        except Conversation.DoesNotExist:
            await asyncio.sleep(HOUR)
            continue

        message = 'Давно тебя не было в уличных гонках! Заходи!'

        for conversation in conversations:
            ts = int(time())
            if ts - conversation.last_ts >= DAY * 2:
                await write(conversation.id, message)

        await asyncio.sleep(HOUR)
