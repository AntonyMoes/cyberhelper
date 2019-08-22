from os import environ
from bot import Bot


if __name__ == '__main__':
    try:
        token = environ['API_KEY']
    except KeyError:
        exit(1)

    bot = Bot(token)

    print('Бот запущен')
    bot.run()
