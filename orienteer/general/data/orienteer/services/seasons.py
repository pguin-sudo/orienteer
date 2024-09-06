from ..models.seasons import Season
from ..repositories import seasons
from ..database import database_helper


async def get_seasons() -> tuple[Season, ...]:
    async with database_helper.session_factory() as db_session:
        return await seasons.get_seasons(db_session)


async def get_current_season() -> Season:
    async with database_helper.session_factory() as db_session:
        return await seasons.get_current_season(db_session)
    