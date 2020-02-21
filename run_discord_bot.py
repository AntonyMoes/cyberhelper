from os import environ
from bot import DiscordBot
from utils import get_env_var


if __name__ == '__main__':
    try:
        token = environ['DISC_TOKEN']
    except KeyError:
        exit(1)

    pg_user = get_env_var('POSTGRES_USER', 'postgres')
    pg_password = get_env_var('POSTGRES_PASSWORD', '')
    pg_database = get_env_var('POSTGRES_DB', 'postgres')
    pg_host = get_env_var('PGHOST', 'localhost')

    client = DiscordBot()
    print('Бот запущен')
    client.run(token)
