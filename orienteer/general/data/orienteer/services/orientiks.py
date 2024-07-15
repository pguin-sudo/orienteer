"""
async def get_balance_raw_info(user_id: UUID) -> dict | None:
    async with DBConnectionContextManager() as connection:
        return await connection.fetchrow('SELECT * FROM orientiks WHERE user_id = $1::uuid', user_id)


async def add_time_balancing(user_id: UUID, time_balancing: int) -> None:
    async with DBConnectionContextManager() as connection:
        return await connection.execute('INSERT INTO orientiks (user_id, time_balancing) VALUES ($1, $2)', user_id,
                                        time_balancing)


async def set_orientiks_from_friends(user_id: UUID, amount: int) -> None:
    async with DBConnectionContextManager() as connection:
        return await connection.execute('UPDATE orientiks SET friends = $1 where user_id = $2', amount, user_id)


async def add_spent(user_id: UUID, amount: int) -> None:
    async with DBConnectionContextManager() as connection:
        current_spent = await connection.fetchval('SELECT spent FROM orientiks WHERE user_id = $1', user_id)

        new_spent = current_spent + amount

        await connection.execute('UPDATE orientiks SET spent = $1 WHERE user_id = $2', new_spent, user_id)
"""

import asyncio
from uuid import UUID

# orientiks per hour
price = 2
price_for_init = 1.3  # was 1.95


async def _init_balance(user_id: UUID) -> None:
    # TODO: FIX THIS
    return
    overall = await ss14.get_playtime_timedelta(user_id=user_id, tracker='Overall')
    await ss14.add_time_balancing(user_id, int(overall.total_seconds() // 3600 * price_for_init))


async def get_balance(user_id: UUID) -> int:
    # TODO: FIX THIS
    return 69
    overall = await ss14.get_playtime_timedelta(user_id=user_id, tracker='Overall')

    if overall is None:
        return 0

    raw_info = await ss14.get_balance_raw_info(user_id=user_id)
    if raw_info is None:
        await _init_balance(user_id)
        raw_info = await ss14.get_balance_raw_info(user_id=user_id)

    fine = sum([await formulas.calculate_fine(ban['expiration_time'] - ban['ban_time']) for ban in
                await ss14.get_bans(user_id=user_id) if ban['expiration_time'] is not None])

    return int(overall.total_seconds() // 3600 * price
               + raw_info['sponsorship']
               + raw_info['friends']
               + raw_info['pardons']
               - raw_info['time_balancing']
               - raw_info['spent']
               - fine)
