from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.orientiks_cached_info import OrientiksCachedInfo


async def add_cached_info(db_session: AsyncSession, cached_playtime: OrientiksCachedInfo):
    db_session.add(cached_playtime)
    await db_session.commit()


async def get_all_cached_info(db_session: AsyncSession) -> tuple[OrientiksCachedInfo, ...]:
    result = await db_session.execute(select(OrientiksCachedInfo))
    return tuple(result.scalars().all())


async def get_cached_info(db_session: AsyncSession, timestamp: datetime) -> OrientiksCachedInfo:
    stmt = select(OrientiksCachedInfo).where(OrientiksCachedInfo.date <= timestamp).order_by(
        OrientiksCachedInfo.date.desc()).limit(1)
    result = await db_session.execute(stmt)
    cached_info = result.scalars().first()
    return cached_info
