from uuid import UUID
from ..dbhandler import DBHandler


async def get_admin_rank_id(user_id: UUID) -> int | None:
    async with DBHandler() as connection:
        result = await connection.fetchval('SELECT admin_rank_id FROM admin WHERE user_id = $1', user_id)
        return int(result) if result is not None else None


async def get_rank_name(admin_rank_id: int) -> str | None:
    async with DBHandler() as connection:
        return str(await connection.fetchval('SELECT name FROM admin_rank WHERE admin_rank_id = $1', admin_rank_id))
