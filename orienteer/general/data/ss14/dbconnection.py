import asyncpg
from asyncpg.pool import Pool

from orienteer.general.config import (
    POSTGRES_SS14_HOST,
    POSTGRES_SS14_PORT,
    POSTGRES_SS14_DBNAME,
    POSTGRES_SS14_USER,
    POSTGRES_SS14_PASSWORD,
)


class DBConnectionContextManager:
    _pool: Pool | None = None

    async def __aenter__(self) -> asyncpg.Connection:
        if DBConnectionContextManager._pool is None:
            DBConnectionContextManager._pool = await asyncpg.create_pool(
                user=POSTGRES_SS14_USER,
                password=POSTGRES_SS14_PASSWORD,
                host=POSTGRES_SS14_HOST,
                port=POSTGRES_SS14_PORT,
                database=POSTGRES_SS14_DBNAME,
            )
        self.connection = await DBConnectionContextManager._pool.acquire()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if DBConnectionContextManager._pool is not None:
            await DBConnectionContextManager._pool.release(self.connection)
        self.connection = None
