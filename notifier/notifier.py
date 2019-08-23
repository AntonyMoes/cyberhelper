from base import BaseBot
import notifier.notifications as nf


class Notifier(BaseBot):
    def __init__(self, token: str, pg_user: str, pg_password: str, pg_database: str, pg_host: str):
        super().__init__(token, pg_user, pg_password, pg_database, pg_host)

    async def run(self):
        coros = [
            nf.girl_notification(self.write_msg),
            nf.absent_notification(self.write_msg),
        ]

        await self._run(coros)
