import heapq
from datetime import timedelta
from typing import Tuple, Any
from uuid import UUID

from orienteer.general.data.orienteer.database import async_session
from orienteer.general.data.orienteer.models.seasons_cached_playtime import CachedPlaytime
from orienteer.general.data.orienteer.repositories import seasons_cached_playtime
from orienteer.general.data.ss14.repositories import playtime, player


async def get_cached_playtime(season_id: int, user_id: UUID):
    async with async_session() as db_session:
        return await seasons_cached_playtime.get_cached_playtime(db_session, season_id, user_id)


async def _process_user(user_id: UUID, season_id: int, db_session) -> playtime:
    overall_playtime = await playtime.get_tracker(user_id, 'Overall')
    if overall_playtime is None:
        return timedelta()

    cached_playtime = await seasons_cached_playtime.get_cached_playtime(db_session, season_id, user_id)
    if cached_playtime is None:
        await seasons_cached_playtime.add_cached_playtime(db_session,
                                                          CachedPlaytime(user_id, overall_playtime['time_spent'],
                                                                         season_id))
        return timedelta()

    return overall_playtime['time_spent'] - cached_playtime.playtime


async def get_leaderboard(season_id: int, depth: int = 7) -> Tuple[Tuple[UUID, Any], ...]:
    leaderboard = []

    async with async_session() as db_session:
        async for user_id in player.all_user_ids_generator():
            leaderboard.append((user_id, await _process_user(user_id, season_id, db_session)))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    return tuple(leaderboard[:7])
