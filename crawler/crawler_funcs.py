import asyncio
from math import inf

from orm.models import Conversation
from utils import MINUTE


async def load_conversations(api):
    BATCH = 200
    offset = 0
    count = inf
    conversations = []

    while offset < count:
        conversation_info = await api('messages.getConversations', offset=offset, count=BATCH)
        count = conversation_info['count']
        conversations += conversation_info['items']

        offset += BATCH

    for conversation in conversations:
        conv_id = conversation['conversation']['peer']['id']
        ts = conversation['last_message']['date']
        try:
            await Conversation.objects.filter(id=conv_id)
        except Conversation.DoesNotExist:
            await Conversation.objects.create(id=conv_id, last_ts=ts)


async def update_names(api):
    while True:
        try:
            conversations = await Conversation.objects.get()
        except Conversation.DoesNotExist:
            await asyncio.sleep(MINUTE * 10)
            continue

        ids = []
        for conversation in conversations:
            ids.append(conversation.id)

        # todo: it is possible to get up to 1000 users at a time, handle it
        info = await api('users.get', user_ids=','.join([str(id) for id in ids]))

        for conv_info, conversation in zip(info, conversations):
            conversation.name = conv_info['first_name']
            await conversation.save()

        await asyncio.sleep(MINUTE * 10)
