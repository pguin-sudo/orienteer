from uuid import UUID
from ..dbconnection import DBConnectionContextManager


async def is_discord_linked(user_id: UUID) -> bool:
    async with DBConnectionContextManager() as connection:
        discord_user_id = await connection.fetchval("SELECT discord_user_id FROM discord_auth WHERE user_id::uuid = $1",
                                                    user_id)
        return bool(discord_user_id)


async def link_discord(user_id: UUID, discord_user_id: int, discord_username: str) -> None:
    async with DBConnectionContextManager() as connection:
        await connection.fetchval(
            "INSERT INTO discord_auth (user_id, discord_user_id, discord_username) VALUES ($1::uuid, $2, $3::text)",
            user_id, discord_user_id, discord_username)
