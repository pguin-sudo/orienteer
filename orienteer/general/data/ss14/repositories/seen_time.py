from uuid import UUID
from datetime import datetime

from ..dbconnection import DBConnectionContextManager


async def get_last_seen_time(user_id: UUID) -> datetime | None:
    async with DBConnectionContextManager() as connection:
        return await connection.fetchval('SELECT last_seen_time FROM player WHERE user_id = $1', user_id)


async def get_first_seen_time(user_id: UUID) -> datetime | None:
    async with DBConnectionContextManager() as connection:
        return await connection.fetchval('SELECT first_seen_time FROM player WHERE user_id = $1', user_id)
