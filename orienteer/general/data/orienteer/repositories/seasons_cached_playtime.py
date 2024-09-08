from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.seasons_cached_playtime import CachedPlaytime


async def add_cached_playtime(
    db_session: AsyncSession, cached_playtime: CachedPlaytime
):
    db_session.add(cached_playtime)
    await db_session.commit()


async def get_cached_playtime(
    db_session: AsyncSession, season_id: int, user_id: UUID
) -> CachedPlaytime:
    result = await db_session.execute(
        select(CachedPlaytime).where(
            user_id == CachedPlaytime.user_id, season_id == CachedPlaytime.season_id
        )
    )
    return result.scalar_one_or_none()
