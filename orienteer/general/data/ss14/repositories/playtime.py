from datetime import timedelta
from uuid import UUID

from orienteer.general.data.orienteer.services import transactions
from ..dbconnection import DBConnectionContextManager


async def get_playtime_timedelta(user_id: UUID, tracker: str) -> timedelta | None:
    async with DBConnectionContextManager() as connection:
        return await connection.fetchval(
            f"SELECT time_spent FROM play_time WHERE player_id = $1 and tracker = $2",
            user_id,
            tracker,
        )


async def add_playtime(user_id: UUID, tracker: str, minutes: int):
    async with DBConnectionContextManager() as connection:
        current_time = await connection.fetchval(
            f"SELECT time_spent FROM play_time WHERE player_id = $1 and tracker = $2",
            user_id,
            tracker,
        )
        if current_time:
            await connection.fetchval(
                "UPDATE play_time SET time_spent = $1 WHERE player_id = $2 AND tracker = $3",
                timedelta(minutes=current_time.total_seconds() / 60 + minutes),
                user_id,
                tracker,
            )
        else:
            await connection.fetchval(
                "INSERT INTO play_time (tracker, player_id, time_spent) VALUES ($1, $2, $3)",
                tracker,
                user_id,
                (timedelta(minutes=minutes)),
            )


async def get_all_trackers(user_id: UUID) -> list:
    async with DBConnectionContextManager() as connection:
        return await connection.fetch(
            "SELECT * FROM play_time WHERE player_id = $1", user_id
        )


async def get_most_popular_tracker(user_id: UUID) -> dict | None:
    async with DBConnectionContextManager() as connection:
        query = """
            SELECT *
            FROM play_time
            WHERE player_id = $1 AND tracker != 'Overall'
            ORDER BY time_spent DESC
            LIMIT 1
        """
        return await connection.fetchrow(query, user_id)


async def get_tracker(user_id: UUID, tracker: str) -> dict | None:
    async with DBConnectionContextManager() as connection:
        query = """
            SELECT *
            FROM play_time
            WHERE player_id = $1 AND tracker = $2
            ORDER BY time_spent DESC
            LIMIT 1
        """
        return await connection.fetchrow(query, user_id, tracker)
