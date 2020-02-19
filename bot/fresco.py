from random import choice
from aiohttp import request
import asyncio
from selectolax.parser import HTMLParser, Node

from utils import user_agent

SITE = 'https://ru.citaty.net/avtory/zhak-fresko/?page='
PAGES = list(range(1, 8))


async def get_fresco(user_name: str) -> str:
    async with request('GET', SITE + str(choice(PAGES)), headers={'User-Agent': user_agent}) as resp:
        text = await resp.text()
        quote_nodes = HTMLParser(text).css('a[data-quote-content]')
        quote_node = choice(quote_nodes)
        impure_quote: str = quote_node.attributes['title']
        quote = impure_quote[18:impure_quote.find('“')]
        return quote


if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(get_fresco('ТОХА')))
