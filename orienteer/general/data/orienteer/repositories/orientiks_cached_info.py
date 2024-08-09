from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.orientiks_cached_info import OrientiksCachedInfo


async def add_cached_info(db_session: AsyncSession, cached_playtime: OrientiksCachedInfo):
    db_session.add(cached_playtime)
    await db_session.commit()


async def get_all_cached_info(db_session: AsyncSession) -> tuple[OrientiksCachedInfo, ...]:
    result = await db_session.execute(select(OrientiksCachedInfo))
    return tuple(result.scalars().all())


async def get_last_cached_info(db_session: AsyncSession) -> OrientiksCachedInfo:
    result = await db_session.execute(select(OrientiksCachedInfo).order_by(OrientiksCachedInfo.date.desc()).limit(1))
    return result.scalars().one_or_none()
