"""
async def get_users_by_promo_code(code: str) -> int:
    async with DBHandler() as connection:
        return len(await connection.fetch("SELECT user_id FROM promo_cache WHERE code = $1::text", code))


async def get_cringe_usages_by_promo_code(code: str) -> int:
    async with DBHandler() as connection:
        return await connection.fetchval("SELECT usages FROM promos WHERE code = $1::text", code)
"""
