from datetime import datetime
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orienteer.general.data.orienteer.models.seasons import Season


async def get_current_season(db_session: AsyncSession) -> Season:
    current_date = datetime.now()
    season = await db_session.execute(
        select(Season).where(Season.start_date <= current_date).order_by(Season.start_date.desc()))
    return season.scalar_one_or_none()


async def get_seasons(db_session: AsyncSession) -> tuple[Season, ...]:
    seasons = await db_session.execute(select(Season).order_by(Season.start_date.desc()))
    return tuple(seasons.scalars().all())
