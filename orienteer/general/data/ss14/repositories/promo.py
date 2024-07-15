from uuid import UUID
from ..dbhandler import DBHandler


async def check_dependencies(user_id: UUID, dependencies: dict) -> bool:
    async with DBHandler() as connection:
        for tracker, time_needed in dependencies.items():
            time = await connection.fetchval("SELECT time_spent FROM play_time "
                                             "WHERE player_id = $1 and tracker = $2", user_id, tracker)
            if not time or time.total_seconds() / 60 < time_needed:
                return False
        return True
