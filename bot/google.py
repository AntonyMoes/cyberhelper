from urllib.parse import quote
from selectolax.parser import HTMLParser
import aiohttp

from utils import user_agent

base_query = 'https://google.com/search?q='


async def google_it(query: str, how_many: int = 1) -> str:
    async with aiohttp.request('GET', base_query + quote(query), headers={'User-Agent': user_agent}) as resp:
        text = await resp.text()
        i = 0

        results = []
        search_result_node = HTMLParser(text).css_first('div[eid]')
        if search_result_node is None:
            return 'Ничего не нашел'

        nodes = search_result_node.css_first('div > div.srg').css_first('div.srg').css('div.g')
        for node in nodes:
            node = node.css_first('div[data-ved]').css_first('div.rc')
            header_node = node.css_first('div.r').css_first('a')

            url = header_node.attributes['href']

            header_node = node.css_first('h3').css_first('div')

            title = header_node.text().strip()

            print(f'{i}: {title} {url}')
            results.append(f'Описание: {title}\nСсылка: {url}\n')
            i += 1

    if len(results) > 0:
        return '\n'.join(results[:how_many])
    else:
        return 'Ничего не нашел'
