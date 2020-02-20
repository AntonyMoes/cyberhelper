import asyncio
from typing import List
from os import environ

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
accept_language = 'ru-RU;q=0.8,ru;q=0.7'


def get_env_var(name: str, default=None):
    try:
        return environ[name]
    except KeyError:
        return default


def split_message(message: str, threshold: int, sep: str = '\n') -> List[str]:
    def chunkify(msg: str) -> List[str]:
        return [msg[i:i + threshold] for i in range(0, len(msg), threshold)]

    chunks = chunkify(message)

    def sift(curr_idx, msg):
        nonlocal chunks
        if curr_idx < len(chunks) - 1:
            new_chunks = chunkify(msg + chunks[curr_idx + 1])
            new_chunk = new_chunks[0]

            chunks[curr_idx + 1] = new_chunk
            if len(new_chunks) > 1:
                sift(curr_idx + 1, new_chunks[1])
        else:
            chunks += chunkify(msg)

    messages = []
    for i, chunk in enumerate(chunks):
        idx = chunk.rfind(sep)

        if idx <= 0 or len(chunk) < threshold:  # or idx < threshold / 2:
            messages.append(chunk)
            continue
        else:
            first, second = chunk[:idx], chunk[idx+1:]
            messages.append(first)
            sift(i, second)

    stripped = list(map(lambda s: s.strip(sep), messages))
    return stripped


if __name__ == '__main__':
    print(*split_message('qwerty\nwefsdgdfgfdg\ndsf\ns\neretrytyh\nwerwe', 6), sep='|')
    print()
    print(*split_message('qwerty\nwefsdgdfgfdg\ndsf\ns\neretrytyh\nwerwe', 25), sep='|')
