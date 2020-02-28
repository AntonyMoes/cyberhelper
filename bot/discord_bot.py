import discord
from random import randint
from bot.commands import check_command, process_command, Command
from bot.ads import get_ad
from generator import Generator
import re

# REPLY = ['pong'] * 9 + ['В ЖОПУ СЕБЕ СВОЙ ПИГ ЗАСУНЬ ГНИДА']
PREFIX ='<@!680539076021321729>'

gen = Generator('trained_data/cyber_weights')
regex = re.compile('[ ,;.]')


async def process_msg(text: str) -> str:
    text = text[len(PREFIX):]
    if regex.match(text[0]):
        print('REGEX')
        text = text[1:]

    text = text.lower().strip()

    command, info = check_command(text)
    if command != Command.Unknown:
        try:
            return (await process_command(None, command, info, None))[0]
        except ValueError:
            return f'Неправильные параметры({info}) для команды "{command.value}"'

    is_ad = randint(1, 15) == 1
    if is_ad:
        return get_ad()

    return gen.generate(seed=text, size=randint(10, 80))


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        # print(type(message))
        # print(message)
        # print(type(message.channel))
        # print(message.channel)
        # print(message.content)

        # return
        # don't respond to ourselves
        if message.author == self.user:
            return

        text: str = message.content
        if not text.startswith(PREFIX):
            return

        resp = await process_msg(text)
        if len(resp) == 0:
            await message.channel.send('нахуй иди')

        await message.channel.send(resp)

