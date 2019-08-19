from string import Template
from random import randint

quotes = [
    Template('Я городской $who, $what не имею.'),
    Template('Твоя $who?'),
    Template('Хорошего дня, $who.'),
    Template('Просто не люблю общение в таком тоне.'),
    Template('Зачем тогда вообще было писать в эту беседу?'),
    Template('$who к успеху шел, не получилось, не фортануло.'),
    Template('...'),
    Template('$who есть.'),
    Template('Это уже $who.'),
    Template('Зачем устраиваешь театр $what?'),
    Template('$who с большой буквы надо было.'),
    Template('Может надо выйти на $what или даже $what.'),
]

whos = [
    'телка',
    'суслик',
    'противоречие',
    'пацан',
    'абсурдизм',
    'абсурд',
    'житель',
    '👌',
    'Александр',
    'куратор',
    'замдек',
]

whats = [
    'телок',
    'сусликов',
    'противоречия',
    'пацана',
    'абсурдизма',
    'абсурда',
    'жителя',
    '👌',
    'Александра',
    'куратора',
    'замдека',
]


def get_quote() -> str:
    d = dict()
    d['who'] = whos[randint(0, len(whos) - 1)]
    d['what'] = whats[randint(0, len(whats) - 1)]

    t = quotes[randint(0, len(quotes) - 1)]
    s = t.safe_substitute(d)
    s = s[0].upper() + s[1:]
    return s


if __name__ == '__main__':
    print(get_quote())
