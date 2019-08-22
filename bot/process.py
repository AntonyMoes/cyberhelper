from bot.quotes import get_quote
from bot.ads import get_ad
from generator import Generator
from random import randint

generator = Generator('trained_data/cyber_weights')


def process_command(message: str) -> str:
    is_ad = randint(1, 15) == 1
    if is_ad:
        return get_ad()

    if message.find('цитата') != -1:
        return get_quote()
    else:
        return generator.generate(seed=message, size=randint(10, 80))
