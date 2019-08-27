from enum import Enum
from random import randint
from collections import namedtuple
from pydoc import locate
from typing import List, Optional

from bot.quotes import get_quote
from bot.jokes import get_joke, get_bash_joke
from bot.google import google_it
from bot.business import get_advice
from bot.weather import get_weather
from orm.models import Conversation

CommandData = namedtuple('CommandData', ['name', 'patterns', 'description'])


class Command(Enum):
    Help = CommandData('Помощь', ['помощь'], 'список команд')
    Quote = CommandData('Цитата', ['цитата'], 'народная мудрость')
    Joke = CommandData('Шутка', ['шутка'], 'смешинка из интернета или личных архивов')
    GoogleMany = CommandData('Погугли много',
                             ['погугли <query>, дай <n:int> результатов',
                              'погугли <query>, дай <n:int> результата',
                              'погугли <query>, дай <n:int> результат'],
                             'поиск большего количества информации в интернете')
    Google = CommandData('Погугли', ['погугли <query>', 'погуглишь <query>?'], 'поиск информации в интернете')
    Advice = CommandData('Совет', ['совет', 'дай совет', 'яви свою мудрость'], 'узнайте, как развить себя и бизнес')
    Weather = CommandData('Погода',
                          ['погода <place>', 'вот скажи, какая погода в <place>, а?',
                           'скажи, какая погода в <place>?', 'скажи, какая погода в <place>'],
                          'погода в интересующем вас месте')
    StrikeBack = CommandData('Огрызнуться', ['ты <smth>'], 'огрызнуться в ответ')

    Unknown = CommandData('', [], '')


PARAM_OPEN = '<'
PARAM_CLOSE = '>'
TYPE_DEFINITION = ':'


def __check_brackets():
    for command in list(Command):
        patterns: List[str] = command.value.patterns
        for p in patterns:
            opens = p.count(PARAM_OPEN)
            closes = p.count(PARAM_CLOSE)
            if opens != closes:
                raise ValueError(f'Bracket count mismatch in pattern {p}')

            if opens != 0:
                if p.find(PARAM_OPEN) > p.find(PARAM_CLOSE):
                    raise ValueError(f'Bracket closes before it\'s opened in pattern {p}')


def __check_types():
    for command in list(Command):
        patterns: List[str] = command.value.patterns
        for p in patterns:
            var_start = p.find(PARAM_OPEN)

            # searching varibale
            while var_start != -1:
                var_end = p.find(PARAM_CLOSE, var_start)
                type_pos = p.find(TYPE_DEFINITION, var_start, var_end)

                # check if has type
                if type_pos != -1:
                    type_str = p[type_pos + 1: var_end]
                    if locate(type_str) is None:
                        raise ValueError(f'Improper type provided in pattern {p}')

                var_start = p.find(PARAM_OPEN, var_end)


__check_brackets()
__check_types()


def _check_pattern(p: str, message: str) -> Optional[dict]:
    params = {}

    p_iter = 0
    m_iter = 0
    while p_iter < len(p):
        if p[p_iter] == PARAM_OPEN:
            param_start = p_iter + 1
            param_end = p.find(PARAM_CLOSE, param_start)

            name_and_type = p[param_start: param_end].split(':')
            param_name = name_and_type[0]
            if len(name_and_type) > 1:
                param_type = locate(name_and_type[1])
            else:
                param_type = str

            postfix_end = postfix_start = param_end + 1
            while postfix_end < len(p) and p[postfix_end] != PARAM_OPEN :
                postfix_end += 1
            postfix = p[postfix_start: postfix_end]

            param_value_start = m_iter
            param_value_end = message.rfind(postfix, param_value_start)
            if param_value_end == -1:
                # message doesn't match the pattern
                return

            try:
                param_value = param_type(message[param_value_start: param_value_end])
            except ValueError:
                # wrong param type
                return

            if param_value == '':
                # empty param
                return

            params[param_name] = param_value

            p_iter = postfix_end
            m_iter = param_value_end + len(postfix)
            continue

        if p[p_iter].lower() != message[m_iter].lower():
            # message doesn't match the pattern
            return

        p_iter += 1
        m_iter += 1

    return params


def _parse_command(message: str, command: Command) -> Optional[dict]:
    for p in command.value.patterns:
        params = _check_pattern(p, message)
        if params is not None:
            return params


def check_command(message: str) -> (Command, dict):
    for command in list(Command):
        if command == Command.Unknown:
            continue

        params = _parse_command(message, command)
        if params is not None:
            return command, params

    return Command.Unknown, {}


async def help_processor(api, params: dict, user_id: int) -> (str, str):
    descriptions = []
    for c in list(Command):
        if c == Command.Unknown:
            continue

        data: CommandData = c.value
        description = f'{data.name} - {data.description}\nСинтаксис: {", ".join(data.patterns)}'
        descriptions.append(description)

    result = 'Список команд:\n\n' + '\n\n'.join(descriptions)
    return result, ''


async def quote_processor(api, params: dict, user_id: int) -> (str, str):
    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    reply = get_quote(user_name)

    return reply, ''


async def joke_processor(api, params: dict, user_id: int) -> (str, str):
    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    rand = randint(0, 10)
    if rand == 0:
        reply = get_joke(user_name)
    else:
        reply = await get_bash_joke()

    return reply, ''


async def google_processor(api, params: dict, user_id: int) -> (str, str):
    query = params['query']
    reply = await google_it(query)

    return reply, ''


async def google_many_processor(api, params: dict, user_id: int) -> (str, str):
    n = params['n']
    query = params['query']

    reply = await google_it(query, n)

    return reply, ''


async def advice_processor(api, params: dict, user_id: int) -> (str, str):
    attachment = await get_advice(api)

    return '', attachment


async def weather_processor(api, params: dict, user_id: int) -> (str, str):
    place = params['place']
    reply = await get_weather(place)

    return reply, ''


async def strike_back_processor(api, params: dict, user_id: int) -> (str, str):
    smth = params['smth']

    conversation = await Conversation.objects.filter(id=user_id).get_one()
    user_name = conversation.name

    reply = f'{user_name}, сам(а) ты {smth}!'

    return reply, ''


_command_processors = {
    Command.Help: help_processor,
    Command.Quote: quote_processor,
    Command.Joke: joke_processor,
    Command.Google: google_processor,
    Command.GoogleMany: google_many_processor,
    Command.Advice: advice_processor,
    Command.Weather: weather_processor,
    Command.StrikeBack: strike_back_processor,
}


async def process_command(api, command: Command, params: dict, user_id: int) -> (str, str):
    print(f'Command: {command.value.name}\nParams: {params}')

    if command == Command.Unknown:
        raise TypeError('Valid command type expected')

    return await _command_processors[command](api, params, user_id)
