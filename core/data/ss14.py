import datetime
from datetime import timedelta
from typing import AsyncGenerator
from uuid import UUID

from core.data.database import DBHandler


# nickname - user_id - discord_user_id

# BASIC


async def get_user_id(nickname: str) -> UUID | None:
    async with DBHandler() as connection:
        result = await connection.fetchval("SELECT user_id FROM player WHERE last_seen_user_name = $1::text", nickname)
        if result is not None:
            user_id = UUID(str(result))
            return user_id
        else:
            return None


async def get_ckey(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        result = await connection.fetchval("SELECT last_seen_user_name FROM player WHERE user_id = $1::uuid", user_id)
        if result is not None:
            user_name = str(result)
            return user_name
        else:
            return None


async def get_discord_user_id_by_user_id(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        result = await connection.fetchval("SELECT discord_user_id FROM discord_auth WHERE user_id = $1::uuid", user_id)
    if result is not None:
        discord_user_id = str(result)
        return discord_user_id
    else:
        return None


async def get_user_id_by_discord_user_id(discord_user_id: int) -> UUID | None:
    async with DBHandler() as connection:
        result = await connection.fetchval("SELECT user_id FROM discord_auth WHERE discord_user_id = $1",
                                           discord_user_id)
        if result is not None:
            user_id = str(result)
            return UUID(user_id)
        else:
            return None


# checker
async def is_discord_linked(user_id: UUID) -> bool:
    async with DBHandler() as connection:
        discord_user_id = await connection.fetchval("SELECT discord_user_id FROM discord_auth WHERE user_id::uuid = $1",
                                                    user_id)
        return bool(discord_user_id)


async def link_discord(user_id: UUID, discord_user_id: int, discord_username: str) -> None:
    async with DBHandler() as connection:
        await connection.fetchval(
            "INSERT INTO discord_auth (user_id, discord_user_id, discord_username) VALUES ($1::uuid, $2, $3::text)",
            user_id, discord_user_id, discord_username)


# whitelist
async def check_whitelist(user_id: UUID) -> bool:
    async with DBHandler() as connection:
        return len(await connection.fetch("SELECT * FROM whitelist WHERE user_id = $1", user_id)) > 0


async def delete_from_whitelist(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        return await connection.fetchval("DELETE FROM whitelist WHERE user_id = $1", user_id)


async def add_to_whitelist(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        return await connection.fetchval("INSERT INTO whitelist VALUES ($1)", user_id)


# admin
async def get_admin_rank_id(user_id: UUID) -> int | None:
    async with DBHandler() as connection:
        result = await connection.fetchval(f"SELECT admin_rank_id FROM admin WHERE user_id = '{user_id}'")
        return int(result) if result is not None else None


async def get_rank_name(admin_rank_id: int) -> str | None:
    async with DBHandler() as connection:
        return str(await connection.fetchval(f"SELECT name FROM admin_rank WHERE admin_rank_id = '{admin_rank_id}'"))


# playtime
async def get_playtime_timedelta(user_id: UUID, tracker: str) -> datetime.timedelta:
    async with DBHandler() as connection:
        return await connection.fetchval(f"SELECT time_spent FROM play_time WHERE player_id = $1 and tracker = $2",
                                         user_id, tracker)


async def add_playtime(user_id: UUID, tracker: str, minutes: int) -> None:
    async with DBHandler() as connection:
        current_time = await connection.fetchval(
            f"SELECT time_spent FROM play_time WHERE player_id = $1 and tracker = $2", user_id, tracker)
        if current_time:
            await connection.fetchval("UPDATE play_time SET time_spent = $1 WHERE player_id = $2 AND tracker = $3",
                                      timedelta(minutes=current_time.total_seconds() / 60 + minutes), user_id, tracker)
        else:
            await connection.fetchval("INSERT INTO play_time (tracker, player_id, time_spent) VALUES ($1, $2, $3)",
                                      tracker, user_id, (timedelta(minutes=minutes)))


async def get_all_playtime(user: UUID) -> list:
    async with DBHandler() as connection:
        return await connection.fetch("SELECT * FROM play_time WHERE player_id = $1", user)


# promo
async def get_promo_data(code: str) -> dict:
    async with DBHandler() as connection:
        return await connection.fetchrow("SELECT * FROM promos WHERE code = $1::text", code)


async def check_dependencies(user_id: UUID, dependencies: dict) -> bool:
    async with DBHandler() as connection:
        for tracker, time_needed in dependencies.items():
            time = await connection.fetchval("SELECT time_spent FROM play_time "
                                             "WHERE player_id = $1 and tracker = $2", user_id, tracker)
            if not time or time.total_seconds() / 60 < time_needed:
                return False
        return True


async def check_promo_already_used_discord(discord_user_id: int, code: str) -> bool:
    async with DBHandler() as connection:
        return await connection.fetch("SELECT code FROM promo_cache "
                                      "WHERE discord_user_id = $1 and code = $2", discord_user_id, code)


async def check_promo_already_used_ss14(user_id: UUID, code: str) -> bool:
    async with DBHandler() as connection:
        return await connection.fetch("SELECT code FROM promo_cache WHERE user_id = $1 and code = $2", user_id, code)


async def mark_promo_as_used(user_id: UUID, discord_user_id: int, code: str):
    async with DBHandler() as connection:
        await connection.fetchval('INSERT INTO promo_cache (user_id, discord_user_id, code) VALUES ($1, $2, $3)',
                                  user_id, discord_user_id, code)


async def decrease_promo_usages(code: str):
    async with DBHandler() as connection:
        await connection.fetchval(f"UPDATE promos SET usages = usages - 1 WHERE code = $1", code)


async def get_creator_code(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        creator_codes = await connection.fetch("SELECT code FROM promos WHERE creator = true")
        for creator_code in creator_codes:
            if await connection.fetchval("SELECT code FROM promo_cache WHERE user_id = $1 and code = $2", user_id,
                                         creator_code[0]):
                return str(creator_code[0])
        return None


# profit
async def get_users_by_promo_code(code: str) -> int:
    async with DBHandler() as connection:
        return len(await connection.fetch("SELECT user_id FROM promo_cache WHERE code = $1::text", code))


async def get_cringe_usages_by_promo_code(code: str) -> int:
    async with DBHandler() as connection:
        return await connection.fetchval("SELECT usages FROM promos WHERE code = $1::text", code)


# all char
async def get_user_preference(user_id: UUID) -> dict:
    async with DBHandler() as connection:
        preference = await connection.fetchval("SELECT * FROM preference WHERE user_id = $1", user_id)
        return preference


async def get_user_profiles(preference) -> tuple:
    async with DBHandler() as connection:
        profiles = await connection.fetch("SELECT * FROM profile WHERE preference_id = $1", preference)
        await connection.close()
        return profiles


# BANS
async def get_bans(user_id: UUID) -> tuple:
    async with DBHandler() as connection:
        bans = await connection.fetch('SELECT * FROM server_ban WHERE player_user_id = $1', user_id)

        valid_bans = []
        for ban in bans:
            exists = await connection.fetchval('SELECT EXISTS(SELECT 1 FROM server_unban WHERE ban_id = $1)',
                                               ban['server_ban_id'])
            if not exists:
                valid_bans.append(ban)

        return tuple(valid_bans)


async def get_all_bans_after(ban_id: int) -> tuple:
    async with DBHandler() as connection:
        return await connection.fetch('SELECT * FROM server_ban WHERE server_ban_id > $1 ORDER BY server_ban_id ASC',
                                      ban_id)


async def get_all_rolebans_after(ban_id: int) -> tuple:
    async with DBHandler() as connection:
        return await connection.fetch(
            'SELECT * FROM server_role_ban WHERE server_role_ban_id > $1 ORDER BY server_role_ban_id ASC', ban_id)


async def get_last_ban(user_id: UUID) -> dict | None:
    async with DBHandler() as connection:
        ban_record = await connection.fetchrow(
            'SELECT * FROM server_ban WHERE player_user_id = $1 ORDER BY server_ban_id DESC LIMIT 1', user_id
        )
        if ban_record:
            is_unbanned = await connection.fetchval(
                'SELECT EXISTS(SELECT 1 FROM server_unban WHERE ban_id = $1)', ban_record['server_ban_id']
            )
            if not is_unbanned:
                return dict(ban_record)
            else:
                return None
        else:
            return None


async def add_ban(user_id: UUID, reason: str):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    query = """
        INSERT INTO server_ban (server_ban_id, player_user_id, banning_admin, ban_time, reason)
        VALUES (DEFAULT, $1, $2, $3, $4)
    """
    async with DBHandler() as connection:
        await connection.execute(query, user_id, UUID('00000000-0000-0000-0000-000000000000'), current_time, reason)


# rep
async def fetch_reputation_value(user_id: UUID) -> int:
    async with DBHandler() as connection:
        result = await connection.fetchval('SELECT reputation_value FROM reputations WHERE user_id = $1::uuid', user_id)
        if result is None or not result:
            return 1000
        else:
            return result


# seen_time
async def get_last_seen_time(user_id: UUID) -> datetime.datetime | None:
    async with DBHandler() as connection:
        return await connection.fetchval('SELECT last_seen_time FROM player WHERE user_id = $1::uuid', user_id)


async def get_first_seen_time(user_id: UUID) -> datetime.datetime | None:
    async with DBHandler() as connection:
        return await connection.fetchval('SELECT first_seen_time FROM player WHERE user_id = $1::uuid', user_id)


# orientiks
async def get_balance_raw_info(user_id: UUID) -> dict | None:
    async with DBHandler() as connection:
        return await connection.fetchrow('SELECT * FROM orientiks WHERE user_id = $1::uuid', user_id)


async def add_time_balancing(user_id: UUID, time_balancing: int) -> None:
    async with DBHandler() as connection:
        return await connection.execute('INSERT INTO orientiks (user_id, time_balancing) VALUES ($1, $2)', user_id,
                                        time_balancing)


async def set_orientiks_from_friends(user_id: UUID, amount: int) -> None:
    async with DBHandler() as connection:
        return await connection.execute('UPDATE orientiks SET friends = $1 where user_id = $2', amount, user_id)


async def add_spent(user_id: UUID, amount: int) -> None:
    async with DBHandler() as connection:
        current_spent = await connection.fetchval('SELECT spent FROM orientiks WHERE user_id = $1', user_id)

        new_spent = current_spent + amount

        await connection.execute('UPDATE orientiks SET spent = $1 WHERE user_id = $2', new_spent, user_id)


# extras
async def get_all_user_ids() -> AsyncGenerator[UUID, None]:
    offset = 0

    async with DBHandler() as connection:
        while True:
            query = f'SELECT user_id FROM player LIMIT {1} OFFSET {offset}'
            results = await connection.fetchval(query)
            if not results:
                break
            yield results
            offset += 1