from datetime import datetime

from ..models.seasons import Season
from ..repositories import seasons
from ..database import database_helper


async def get_seasons() -> tuple[Season, ...]:
    async with database_helper.session_factory() as db_session:
        return await seasons.get_seasons(db_session)


async def get_season_by_date(date: datetime) -> Season:
    async with database_helper.session_factory() as db_session:
        return await seasons.get_season(db_session, date)


async def get_seasons_after(date: datetime) -> tuple[Season, ...]:
    async with database_helper.session_factory() as db_session:
        return await seasons.get_seasons_after(db_session, date)
