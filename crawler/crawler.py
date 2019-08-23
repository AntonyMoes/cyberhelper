from base import BaseBot
import crawler.crawler_funcs as cf


class Crawler(BaseBot):
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        super().__init__(token, pg_user, pg_password, pg_database, pg_host)

    async def run(self):
        coros = [
            cf.load_conversations(self._api),
            cf.update_names(self._api),
        ]

        await self._run(coros)
