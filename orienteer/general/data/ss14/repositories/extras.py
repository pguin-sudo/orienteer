from typing import AsyncGenerator
from uuid import UUID

from ..dbconnection import DBConnectionContextManager


async def get_all_user_ids() -> AsyncGenerator[UUID, None]:
    offset = 0

    async with DBConnectionContextManager() as connection:
        while True:
            query = f'SELECT user_id FROM player LIMIT {1} OFFSET {offset}'
            results = await connection.fetchval(query)
            if not results:
                break
            yield results
            offset += 1
