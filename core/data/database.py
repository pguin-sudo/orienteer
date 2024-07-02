import asyncio

import asyncpg
from contextlib import AbstractAsyncContextManager

from core.config import Postgres


class DBHandler(AbstractAsyncContextManager):
    async def __aenter__(self) -> asyncpg.connection:
        self.connection = await asyncpg.connect(user=Postgres.USER,
                                                password=Postgres.PASSWORD,
                                                host=Postgres.HOST,
                                                port=Postgres.PORT,
                                                database=Postgres.DBNAME)
        return self.connection

    async def __aexit__(self, *_):
        await self.connection.close()
