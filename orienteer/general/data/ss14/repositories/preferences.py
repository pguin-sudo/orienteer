from uuid import UUID
from ..dbhandler import DBHandler


async def get_preference(user_id: UUID) -> dict:
    async with DBHandler() as connection:
        preference = await connection.fetchval("SELECT * FROM preference WHERE user_id = $1", user_id)
        return preference
