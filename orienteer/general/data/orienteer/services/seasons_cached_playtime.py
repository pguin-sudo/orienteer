from datetime import timedelta
from typing import Any
from uuid import UUID

from orienteer.general.data.ss14.services import playtime, player
from ..database import database_helper
from ..models.seasons_cached_playtime import CachedPlaytime
from ..repositories import seasons_cached_playtime


async def get_cached_playtime(season_id: int, user_id: UUID):
    async with database_helper.session_factory() as db_session:
        return await seasons_cached_playtime.get_cached_playtime(
            db_session, season_id, user_id
        )


async def _process_user(user_id: UUID, season_id: int, db_session) -> timedelta:
    overall_playtime = await playtime.get_overall(user_id)
    if overall_playtime is None:
        return timedelta()

    cached_playtime = await seasons_cached_playtime.get_cached_playtime(
        db_session, season_id, user_id
    )
    if cached_playtime is None:
        await seasons_cached_playtime.add_cached_playtime(
            db_session, CachedPlaytime(user_id, overall_playtime, season_id)
        )
        return timedelta()

    return overall_playtime - cached_playtime.playtime


async def get_leaderboard(
    season_id: int, depth: int = 7
) -> tuple[tuple[UUID, Any], ...]:
    leaderboard = []

    async with database_helper.session_factory() as db_session:
        async for user_id in player.all_user_ids_generator():
            leaderboard.append(
                (user_id, await _process_user(user_id, season_id, db_session))
            )

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    return tuple(leaderboard[:depth])
