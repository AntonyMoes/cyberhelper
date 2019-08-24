from random import randint
import aiohttp
from selectolax.parser import HTMLParser

from utils import user_agent

jokes = [
    'Подходит Петька к Василиванычу и спрашивает:\n'
    '- Василиваныч, а что такое нюанс?\n'
    'Василиваныч и говорит:\n'
    '- Снимай, Петька, штаны\n'
    'Петька снял.\n'
    'Василиваныч достает х*й и сует Петьке в жопу.'
    'Вот смотри, Петька: у тебя х*й в жопе, и у меня х*й в жопе.\n'
    'Но есть один нюанс!',
]


def get_joke(user_name: str) -> str:
    return jokes[randint(0, len(jokes) - 1)]


async def get_bash_joke() -> str:
    bash = 'https://bash.im/random'

    async with aiohttp.request('GET', bash, headers={'User-Agent': user_agent}) as resp:
        text = await resp.text()
        node = HTMLParser(text).css_first('div.quote__body')
        joke_html: str = node.html
        joke_html = joke_html.replace('<div class="quote__body">', '')
        joke_html = joke_html.replace('</div>', '')
        joke_html = joke_html.strip(' ')
        joke_html = joke_html.strip('\n')
        joke_html = joke_html.strip(' ')
        joke = joke_html.replace('<br>', '\n')

    return joke
