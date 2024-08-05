from uuid import UUID

from ..dbconnection import DBConnectionContextManager


async def get_preference(user_id: UUID) -> dict | None:
    async with DBConnectionContextManager() as connection:
        preference = await connection.fetchval("SELECT * FROM preference WHERE user_id = $1", user_id)
        return preference
