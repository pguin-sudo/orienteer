from uuid import UUID
from ..dbhandler import DBHandler


async def check_whitelist(user_id: UUID) -> bool:
    async with DBHandler() as connection:
        return len(await connection.fetch("SELECT * FROM whitelist WHERE user_id = $1", user_id)) > 0


async def delete_from_whitelist(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        return await connection.fetchval("DELETE FROM whitelist WHERE user_id = $1", user_id)


async def add_to_whitelist(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        return await connection.fetchval("INSERT INTO whitelist VALUES ($1)", user_id)
