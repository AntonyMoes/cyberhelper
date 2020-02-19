from random import randint
import aiohttp
from selectolax.parser import HTMLParser
from html import unescape

from utils import user_agent

jokes = [
    'Колобок повесился'
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
        joke = unescape(joke_html)

    return joke
