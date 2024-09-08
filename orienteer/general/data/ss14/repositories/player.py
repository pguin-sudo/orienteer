from typing import AsyncGenerator
from uuid import UUID

from ..dbconnection import DBConnectionContextManager


async def get_user_id(ckey: str) -> UUID | None:
    async with DBConnectionContextManager() as connection:
        result = await connection.fetchval(
            "SELECT user_id FROM player WHERE last_seen_user_name = $1", ckey
        )
        if result is not None:
            user_id = UUID(str(result))
            return user_id
        else:
            return None


async def get_user_id_nocased(ckey: str) -> tuple[UUID | None, str]:
    async with DBConnectionContextManager() as connection:
        players = await connection.fetch(
            "SELECT user_id, last_seen_user_name FROM player WHERE LOWER(last_seen_user_name) = LOWER($1)",
            ckey,
        )

        if len(players) == 1:
            user_id = UUID(str(players[0]["user_id"]))
            return user_id, players[0]["last_seen_user_name"]
        elif len(players) > 1:
            for player in players:
                if player["user_id"] and player["last_seen_user_name"] == ckey:
                    return UUID(str(player["user_id"])), player["last_seen_user_name"]

        return None, ckey


async def get_ckey(user_id: UUID) -> str | None:
    async with DBConnectionContextManager() as connection:
        result = await connection.fetchval(
            "SELECT last_seen_user_name FROM player WHERE user_id = $1", user_id
        )
        if result is not None:
            user_name = str(result)
            return user_name
        else:
            return None


async def all_user_ids_generator() -> AsyncGenerator[UUID, None]:
    offset = 0
    batch_size = 4

    async with DBConnectionContextManager() as connection:
        while True:
            rows = await connection.fetch(
                f"SELECT user_id FROM player LIMIT {batch_size} OFFSET {offset}"
            )
            if not rows:
                break
            for row in rows:
                yield row["user_id"]
            offset += batch_size


async def all_ckey_generator() -> AsyncGenerator[str, None]:
    offset = 0
    batch_size = 20

    async with DBConnectionContextManager() as connection:
        while True:
            rows = await connection.fetch(
                f"SELECT last_seen_user_name FROM player ORDER BY last_seen_time LIMIT {batch_size} OFFSET {offset}"
            )
            if not rows:
                break
            for row in rows:
                yield row["last_seen_user_name"]
            offset += batch_size
