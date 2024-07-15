from uuid import UUID
from typing import AsyncGenerator

from ..dbhandler import DBHandler


async def get_all_user_ids() -> AsyncGenerator[UUID, None]:
    offset = 0

    async with DBHandler() as connection:
        while True:
            query = f'SELECT user_id FROM player LIMIT {1} OFFSET {offset}'
            results = await connection.fetchval(query)
            if not results:
                break
            yield results
            offset += 1
