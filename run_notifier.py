from os import environ
from utils import get_env_var
import asyncio

from notifier import Notifier

if __name__ == '__main__':
    try:
        token = environ['API_KEY']
    except KeyError:
        exit(1)

    pg_user = get_env_var('PG_USER', 'postgres')
    pg_password = get_env_var('PG_PASSWORD', '')
    pg_database = get_env_var('PG_DATABASE', 'postgres')
    pg_host = get_env_var('PG_HOST', 'localhost')

    notifier = Notifier(token, pg_user=pg_user, pg_password=pg_password, pg_database=pg_database, pg_host=pg_host)

    print('Оповещатель запущен')
    asyncio.get_event_loop().run_until_complete(notifier.run())
