from uuid import UUID
from ..dbconnection import DBConnectionContextManager


async def check(user_id: UUID) -> bool:
    async with DBConnectionContextManager() as connection:
        return len(await connection.fetch("SELECT * FROM whitelist WHERE user_id = $1", user_id)) > 0


async def delete_user(user_id: UUID) -> str | None:
    async with DBConnectionContextManager() as connection:
        return await connection.fetchval("DELETE FROM whitelist WHERE user_id = $1", user_id)


async def add_user(user_id: UUID) -> str | None:
    async with DBConnectionContextManager() as connection:
        return await connection.fetchval("INSERT INTO whitelist VALUES ($1)", user_id)
