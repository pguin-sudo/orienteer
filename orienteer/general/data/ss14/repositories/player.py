from uuid import UUID

from ..dbconnection import DBConnectionContextManager


async def get_user_id(nickname: str) -> UUID | None:
    async with DBConnectionContextManager() as connection:
        result = await connection.fetchval("SELECT user_id FROM player WHERE last_seen_user_name = $1", nickname)
        if result is not None:
            user_id = UUID(str(result))
            return user_id
        else:
            return None


async def get_ckey(user_id: UUID) -> str | None:
    async with DBConnectionContextManager() as connection:
        result = await connection.fetchval("SELECT last_seen_user_name FROM player WHERE user_id = $1", user_id)
        if result is not None:
            user_name = str(result)
            return user_name
        else:
            return None
