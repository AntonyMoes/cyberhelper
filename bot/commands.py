from enum import Enum

from bot.quotes import get_quote
from bot.jokes import get_joke
from orm.models import Conversation


class Command(Enum):
    Help = 'помощь'
    Quote = 'цитата'
    Joke = 'шутка'

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


async def help_processor(info: str, user_id: int) -> str:
    result = 'Список команд:\n' + '\n'.join([c.value for c in list(Command) if c != Command.Unknown])
    return result


async def quote_processor(info: str, user_id: int) -> str:
    if info != '':
        raise ValueError('No info expected')

    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    reply = get_quote(user_name)

    return reply


async def joke_processor(info: str, user_id: int) -> str:
    if info != '':
        raise ValueError('No info expected')

    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    reply = get_joke(user_name)

    return reply


_command_processors = {
    Command.Help: help_processor,
    Command.Quote: quote_processor,
    Command.Joke: joke_processor,
}


async def process_command(command: Command, info: str, user_id: int) -> str:
    if command == Command.Unknown:
        raise TypeError('Valid command type expected')

    return await _command_processors[command](info, user_id)
