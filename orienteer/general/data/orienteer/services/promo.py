from uuid import UUID

from ...ss14.dbhandler import DBHandler  # TODO: FIX THIS SHIT


async def get_promo_data(code: str) -> dict:
    async with DBHandler() as connection:
        return await connection.fetchrow("SELECT * FROM promos WHERE code = $1::text", code)


async def get_creator_code(user_id: UUID) -> str | None:
    async with DBHandler() as connection:
        creator_codes = await connection.fetch("SELECT code FROM promos WHERE creator = true")
        for creator_code in creator_codes:
            if await connection.fetchval("SELECT code FROM promo_cache WHERE user_id = $1 and code = $2", user_id,
                                         creator_code[0]):
                return str(creator_code[0])
        return None

"""     
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
"""
