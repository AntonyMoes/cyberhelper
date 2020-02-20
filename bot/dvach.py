from aiohttp import request
import asyncio
from selectolax.parser import HTMLParser, Node
from typing import Tuple
from Levenshtein import distance
from re import sub

from utils import user_agent

SITE = 'https://2ch.hk'
APP_TEXT = 'Скачать мобильные приложения'


def node_to_title(node: Node) -> Tuple[str, str]:
    text = node.text()
    href = node.attributes['href']
    return text.replace('/', ''), href

TOPIC = '\n|-> '
POST = '\n|   '
MAX_LEN = 70


def process_thread(node: Node) -> Tuple[str, int]:
    op_text = node.css_first('div.thread__oppost > div.post_type_oppost >article.post__message_op').text()
    posts = node.css('div.thread__post')
    texts = [op_text] + list(map(lambda n: n.css_first('article.post__message').text(), posts))
    texts_stripped = list(map(lambda s: s if len(s) < MAX_LEN else s[:MAX_LEN] + '...',
                              map(lambda s: s.replace('\n\t', '').replace('\t', ''),
                                  map(lambda s: sub(r'>>\d+( \(OP\))?', '', s),
                                      texts))))
    # print(texts_stripped)

    return POST.join(map(lambda s: s, texts_stripped)), len(texts)


NUM_TOP = 5


async def get_2ch(board_request: str) -> str:
    async with request('GET', SITE, headers={'User-Agent': user_agent}) as resp:
        text = await resp.text()

        parser = HTMLParser(text)
        # todo add table parsing for nore board options
        list_nodes = parser.css('article > a[href]') + parser.css('li > a[href]')
        list_tuples = list(filter(lambda t: t[0] != APP_TEXT and t[1][-1] == '/', map(node_to_title, list_nodes)))

        list_dist = list(map(lambda t: distance(board_request, t[0]), list_tuples))
        min_dist = min(list_dist)
        prob_board = [t for t, dist in zip(list_tuples, list_dist) if dist == min_dist]

        if len(prob_board) > 1:
            return 'Уточните запрос. Наиболее близки следующие доски:\n' + '\n'.join(map(lambda t: t[0], prob_board))

    board = prob_board[0]
    name, href = board

    async with request('GET', SITE + href, headers={'User-Agent': user_agent}) as resp:
        text = await resp.text()
        parser = HTMLParser(text)
        list_threads = parser.css('div.thread')
        list_processed = list(map(process_thread, list_threads))
        top = list(sorted(list_processed, key=lambda x: x[1], reverse=True))
        top_texts = list(map(lambda x: x[0], top))[:NUM_TOP]

        final = TOPIC.join([name.upper()] + top_texts)

    return final


if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(get_2ch('ВОЛК')))
    print(len(asyncio.get_event_loop().run_until_complete(get_2ch('ВОЛК'))))
    print()
    print(asyncio.get_event_loop().run_until_complete(get_2ch('бред')))
    print(len(asyncio.get_event_loop().run_until_complete(get_2ch('бред'))))
