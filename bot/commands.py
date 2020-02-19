from enum import Enum
from random import randint

from bot.quotes import get_quote
from bot.jokes import get_joke, get_bash_joke
from bot.google import google_it
from bot.business import get_advice
from bot.weather import get_weather
from bot.fresco import get_fresco
from bot.dvach import get_2ch
from orm.models import Conversation


class Command(Enum):
    Help = 'помощь'
    Quote = 'цитата'
    Joke = 'шутка'
    Google = 'погугли'
    GoogleMany = 'погугли_много'
    Advice = 'совет'
    Wisdom = 'мудрость'
    Weather = 'погода'
    Fresco = 'фреско'
    Dvach = 'двач'
    Tooch = '2ch'

    Unknown = ''


def check_command(message: str) -> (Command, str):
    tokens = message.split()
    if len(tokens) == 0:
        tokens = ['']

    try:
        command = Command(tokens[0])
    except ValueError:
        command = Command.Unknown

    if len(tokens) > 1:
        info = ' '.join(tokens[1:])
    else:
        info = ''

    return command, info


async def help_processor(api, info: str, user_id: int) -> (str, str):
    result = 'Список команд:\n' + '\n'.join([c.value for c in list(Command) if c != Command.Unknown])
    return result, ''


async def quote_processor(api, info: str, user_id: int) -> (str, str):
    if info != '':
        raise ValueError('No info expected')

    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    reply = get_quote(user_name)

    return reply, ''


async def joke_processor(api, info: str, user_id: int) -> (str, str):
    if info != '':
        raise ValueError('No info expected')

    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    rand = randint(0, 10)
    if rand == 0:
        reply = get_joke(user_name)
    else:
        reply = await get_bash_joke()

    return reply, ''


async def google_processor(api, info: str, user_id: int) -> (str, str):
    if info == '':
        raise ValueError('Query expected')

    reply = await google_it(info)

    return reply, ''


async def google_many_processor(api, info: str, user_id: int) -> (str, str):
    tokens = info.split()

    if len(tokens) < 2:
        raise ValueError('Not enough arguments')

    how_many = int(tokens[0])
    query = ' '.join(tokens[1:])

    reply = await google_it(query, how_many)

    return reply, ''


async def advice_processor(api, info: str, user_id: int) -> (str, str):
    if info != '':
        raise ValueError('No info expected')

    attachment = await get_advice(api)

    return '', attachment


async def weather_processor(api, info: str, user_id: int) -> (str, str):
    if info == '':
        raise ValueError('Query expected')

    reply = await get_weather(info)

    return reply, ''


async def fresco_processor(api, info: str, user_id: int) -> (str, str):
    if info != '':
        raise ValueError('No info expected')

    reply = await get_fresco(info)

    return reply, ''


async def dvach_processor(api, info: str, user_id: int) -> (str, str):
    if info == '':
        raise ValueError('Board expected')

    reply = await get_2ch(info)

    return reply, ''


_command_processors = {
    Command.Help: help_processor,
    Command.Quote: quote_processor,
    Command.Joke: joke_processor,
    Command.Google: google_processor,
    Command.GoogleMany: google_many_processor,
    Command.Advice: advice_processor,
    Command.Wisdom: advice_processor,
    Command.Weather: weather_processor,
    Command.Fresco: fresco_processor,
    Command.Dvach: dvach_processor,
    Command.Tooch: dvach_processor,
}


async def process_command(api, command: Command, info: str, user_id: int) -> (str, str):
    if command == Command.Unknown:
        raise TypeError('Valid command type expected')

    return await _command_processors[command](api, info, user_id)
