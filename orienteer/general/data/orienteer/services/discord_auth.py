from uuid import UUID

from aiocache import cached
from aiocache.serializers import PickleSerializer

from ..database import database_helper
from ..models.discord_auth import DiscordAuth
from ..repositories import discord_auth


async def is_discord_linked(user_id: UUID) -> bool:
    async with database_helper.session_factory() as db_session:
        return await discord_auth.is_discord_linked(db_session, user_id)


async def link_discord(
    user_id: UUID, discord_user_id: int, discord_username: str
) -> None:
    async with database_helper.session_factory() as db_session:
        await discord_auth.link_discord(
            db_session, user_id, discord_user_id, discord_username
        )


async def get_discord_user_id_by_user_id(user_id: UUID) -> int | None:
    async with database_helper.session_factory() as db_session:
        return await discord_auth.get_discord_user_id_by_user_id(db_session, user_id)


async def get_user_id_by_discord_user_id(discord_user_id: int) -> UUID | None:
    async with database_helper.session_factory() as db_session:
        return await discord_auth.get_user_id_by_discord_user_id(
            db_session, discord_user_id
        )


@cached(ttl=3600, serializer=PickleSerializer())
async def get_all_authorized() -> tuple[DiscordAuth, ...]:
    async with database_helper.session_factory() as db_session:
        return await discord_auth.get_all_authorized(db_session)
