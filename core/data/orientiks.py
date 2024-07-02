import asyncio
from uuid import UUID

from core.data import ss14, formulas

# orientiks per hour
price = 2
price_for_init = 1.3  # was 1.95


async def init_balance(user_id: UUID) -> None:
    overall = await ss14.get_playtime_timedelta(user_id=user_id, tracker='Overall')
    await ss14.add_time_balancing(user_id, int(overall.total_seconds() // 3600 * price_for_init))


async def get_balance(user_id: UUID) -> int:
    overall = await ss14.get_playtime_timedelta(user_id=user_id, tracker='Overall')

    if overall is None:
        return 0

    raw_info = await ss14.get_balance_raw_info(user_id=user_id)
    if raw_info is None:
        await init_balance(user_id)
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
