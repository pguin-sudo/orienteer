from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.discord_auth import DiscordAuth


async def is_discord_linked(db_session: AsyncSession, user_id: UUID) -> bool:
    query = select(DiscordAuth).filter(user_id == DiscordAuth.user_id)
    result = await db_session.execute(query)
    discord_auth = result.scalars().first()
    return discord_auth is not None


async def link_discord(db_session: AsyncSession, user_id: UUID, discord_user_id: int, discord_username: str) -> None:
    discord_auth = DiscordAuth(user_id=user_id, discord_user_id=discord_user_id, discord_username=discord_username)
    db_session.add(discord_auth)
    await db_session.commit()


async def get_discord_user_id_by_user_id(db_session: AsyncSession, user_id: UUID) -> str | None:
    query = select(DiscordAuth.discord_user_id).filter(user_id == DiscordAuth.user_id)
    result = await db_session.execute(query)
    discord_user_id = result.scalar_one_or_none()
    if discord_user_id is not None:
        return str(discord_user_id)
    else:
        return None


async def get_user_id_by_discord_user_id(db_session: AsyncSession, discord_user_id: int) -> UUID | None:
    query = select(DiscordAuth.user_id).filter(discord_user_id == DiscordAuth.discord_user_id)
    result = await db_session.execute(query)
    user_id = result.scalar_one_or_none()
    if user_id is not None:
        return user_id
    else:
        return None
