from random import choice, randint
from time import time
import asyncio

from orm.models import Conversation, Notification
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
    # sleep time if bot failed and restarted right after notification
    sleep_time = randint(HOUR * 8, DAY)
    while True:
        ts = int(time())

        try:
            notification = await Notification.objects.filter(type='girl').get_one()

            time_passed = ts - notification.ts
            # if bot failed and we trying to notify too soon
            if time_passed < sleep_time:
                await asyncio.sleep(sleep_time - time_passed)
                continue

        except Notification.DoesNotExist:
            notification = Notification(type='girl', whom=-1, ts=time())

        try:
            conversations = await Conversation.objects.get()
        except Conversation.DoesNotExist:
            await asyncio.sleep(HOUR)
            continue

        conversation = choice(conversations)
        if len(conversations) > 1:
            while conversation.id == notification.whom:
                conversation = choice(conversations)

        girl = choice(girls)

        if conversation.name is None:
            message = f'Здравствуйте. ' \
                      f'Не могли бы вы узнать, почему {girl} игнорирует меня вконтакте?'
        else:
            message = f'Здравствуйте, {conversation.name}. ' \
                      f'Не могли бы вы узнать, почему {girl} игнорирует меня вконтакте?'

        await write(conversation.id, message)

        notification.whom = conversation.cid
        notification.ts = ts
        await notification.save()

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
