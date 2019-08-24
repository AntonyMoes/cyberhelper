from enum import Enum

from bot.quotes import get_quote


class Command(Enum):
    Quote = 'цитата'
    # Joke = 'шутка'

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


def quote_processor(info: str, user_id: int) -> str:
    if info != '':
        raise ValueError('No info expected')
    reply = get_quote()

    return reply


_command_processors = {
    Command.Quote: quote_processor
}


def process_command(command: Command, info: str, user_id: int) -> str:
    if command == Command.Unknown:
        raise TypeError('Valid command type expected')

    print(command, info, user_id)
    return _command_processors[command](info, user_id)
