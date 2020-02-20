from urllib.parse import quote
from selectolax.parser import HTMLParser
import aiohttp
import asyncio

from utils import user_agent, accept_language

base_query = 'https://google.com/search?q='


async def google_it(query: str, how_many: int = 1) -> str:
    print(base_query + quote(query))
    async with aiohttp.request('GET', base_query + quote(query),
                               headers={'User-Agent': user_agent, 'accept-language': accept_language}) as resp:
        text = await resp.text()

        results = []
        search_result_node = HTMLParser(text).css_first('div[eid]')
        if search_result_node is None:
            return 'Ничего не нашел'

        group_nodes = search_result_node.css('div.srg')
        nodes = [subnode for node in group_nodes for subnode in node.css('div.g')]
        for i, node in enumerate(nodes):
            node = node.css_first('div[data-ved]').css_first('div.rc')
            header_node = node.css_first('div.r').css_first('a')

            url = header_node.attributes['href']
            title_node = node.css_first('h3')
            title = title_node.text().strip()

            print(f'{i}: {title} {url}')
            results.append(f'Описание: {title}\nСсылка: {url}\n')

    if len(results) > 0:
        return '\n'.join(results[:how_many])
    else:
        return 'Ничего не нашел'

if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(google_it('хлеб')))
    print(asyncio.get_event_loop().run_until_complete(google_it('молоко', 5)))
