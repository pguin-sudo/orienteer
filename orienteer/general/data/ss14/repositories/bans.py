from uuid import UUID
from datetime import datetime, timezone

from ..dbconnection import DBConnectionContextManager


async def get_bans(user_id: UUID) -> tuple:
    async with DBConnectionContextManager() as connection:
        bans = await connection.fetch('SELECT * FROM server_ban WHERE player_user_id = $1', user_id)

        valid_bans = []
        for ban in bans:
            exists = await connection.fetchval('SELECT EXISTS(SELECT 1 FROM server_unban WHERE ban_id = $1)',
                                               ban['server_ban_id'])
            if not exists:
                valid_bans.append(ban)

        return tuple(valid_bans)


async def get_all_bans_after(ban_id: int) -> tuple:
    async with DBConnectionContextManager() as connection:
        return await connection.fetch('SELECT * FROM server_ban WHERE server_ban_id > $1 ORDER BY server_ban_id ASC',
                                      ban_id)


async def get_all_role_bans_after(ban_id: int) -> tuple:
    async with DBConnectionContextManager() as connection:
        return await connection.fetch(
            'SELECT * FROM server_role_ban WHERE server_role_ban_id > $1 ORDER BY server_role_ban_id ASC', ban_id)


async def get_last_ban(user_id: UUID) -> dict | None:
    async with DBConnectionContextManager() as connection:
        ban_record = await connection.fetchrow(
            'SELECT * FROM server_ban WHERE player_user_id = $1 ORDER BY server_ban_id DESC LIMIT 1', user_id
        )
        if ban_record:
            is_unbanned = await connection.fetchval(
                'SELECT EXISTS(SELECT 1 FROM server_unban WHERE ban_id = $1)', ban_record[
                    'server_ban_id']
            )
            if not is_unbanned:
                return dict(ban_record)
            else:
                return None
        else:
            return None


async def add_ban(user_id: UUID, reason: str):
    current_time = datetime.now(timezone.utc)
    query = """
        INSERT INTO server_ban (server_ban_id, player_user_id, banning_admin, ban_time, reason)
        VALUES (DEFAULT, $1, $2, $3, $4)
    """
    async with DBConnectionContextManager() as connection:
        await connection.execute(query, user_id, UUID('00000000-0000-0000-0000-000000000000'), current_time, reason)


async def pardon_ban(ban_id: int):
    current_time = datetime.now(timezone.utc)
    query = """
        INSERT INTO server_unban (unban_id, ban_id, unbanning_admin, unban_time)
        VALUES (DEFAULT, $1, $2, $3)
    """
    async with DBConnectionContextManager() as connection:
        await connection.execute(query, ban_id, UUID('00000000-0000-0000-0000-000000000000'), current_time)
