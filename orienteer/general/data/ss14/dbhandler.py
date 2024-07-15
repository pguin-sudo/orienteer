import asyncpg
from contextlib import AbstractAsyncContextManager

from orienteer.general.config.local import (
    POSTGRES_SS14_HOST,
    POSTGRES_SS14_PORT,
    POSTGRES_SS14_DBNAME,
    POSTGRES_SS14_USER,
    POSTGRES_SS14_PASSWORD)


class DBHandler(AbstractAsyncContextManager):
    async def __aenter__(self) -> asyncpg.connection:
        self.connection = await asyncpg.connect(user=POSTGRES_SS14_USER,
                                                password=POSTGRES_SS14_PASSWORD,
                                                host=POSTGRES_SS14_HOST,
                                                port=POSTGRES_SS14_PORT,
                                                database=POSTGRES_SS14_DBNAME)
        return self.connection

    async def __aexit__(self, *_):
        await self.connection.close()
