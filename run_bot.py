from os import environ
from bot import Bot
from utils import get_env_var


if __name__ == '__main__':
    try:
        token = environ['API_KEY']
    except KeyError:
        exit(1)

    pg_user = get_env_var('POSTGRES_USER', 'postgres')
    pg_password = get_env_var('POSTGRES_PASSWORD', '')
    pg_database = get_env_var('POSTGRES_DB', 'postgres')
    pg_host = get_env_var('PG_HOST', 'localhost')

    bot = Bot(token, pg_user=pg_user, pg_password=pg_password, pg_database=pg_database, pg_host=pg_host)

    print('Бот запущен')
    bot.run()
