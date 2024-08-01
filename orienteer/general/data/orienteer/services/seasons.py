from orienteer.general.data.orienteer.models.seasons import Season
from orienteer.general.data.orienteer.repositories import seasons
from ..database import async_session


async def get_seasons():
    async with async_session() as db_session:
        return await seasons.get_seasons(db_session)


async def get_current_season() -> Season:
    async with async_session() as db_session:
        return await seasons.get_current_season(db_session)
