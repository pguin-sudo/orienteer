from uuid import UUID

from ..database import async_session
from ..repositories import discord_auth


async def is_discord_linked(user_id: UUID) -> bool:
    async with async_session() as db_session:
        return await discord_auth.is_discord_linked(db_session, user_id)


async def link_discord(user_id: UUID, discord_user_id: int, discord_username: str) -> None:
    async with async_session() as db_session:
        await discord_auth.link_discord(db_session, user_id, discord_user_id, discord_username)


async def get_discord_user_id_by_user_id(user_id: UUID) -> str | None:
    async with async_session() as db_session:
        return await discord_auth.get_discord_user_id_by_user_id(db_session, user_id)


async def get_user_id_by_discord_user_id(discord_user_id: int) -> UUID | None:
    async with async_session() as db_session:
        return await discord_auth.get_user_id_by_discord_user_id(db_session, discord_user_id)
