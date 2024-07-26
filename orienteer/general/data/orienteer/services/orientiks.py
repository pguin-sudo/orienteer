from uuid import UUID

from orienteer.general.utils.calculations import calculate_fine

from ..repositories import orientiks
from ...ss14.repositories import playtime, bans

from ..database import async_session

price = 2
price_for_init = 1.3  # was 1.95


async def _init_balance(user_id: UUID) -> None:
    overall = await playtime.get_playtime_timedelta(user_id=user_id, tracker='Overall')
    async with async_session() as db_session:
        await orientiks.add_time_balancing(db_session, user_id, int(overall.total_seconds() // 3600 * price_for_init))


async def get_balance(user_id: UUID) -> int:
    overall = await playtime.get_playtime_timedelta(user_id=user_id, tracker='Overall')

    if overall is None:
        return 0

    async with async_session() as db_session:
        raw_info = await orientiks.get_balance_raw_info(db_session, user_id=user_id)
        if raw_info is None:
            await _init_balance(user_id)
            raw_info = await orientiks.get_balance_raw_info(db_session, user_id=user_id)

    fine = sum([calculate_fine(ban['expiration_time'] - ban['ban_time']) for ban in
                await bans.get_bans(user_id=user_id) if ban['expiration_time'] is not None])

    return int(overall.total_seconds() // 3600 * price
               + raw_info.sponsorship
               + raw_info.friends
               + raw_info.pardons
               - raw_info.time_balancing
               - raw_info.spent
               - fine)


async def do_transfer(sender_user_id: UUID, recipient_user_id: UUID, amount: int) -> None:
    async with async_session() as db_session:
        await orientiks.add_orientiks_from_friends(db_session, sender_user_id, -amount)
        await orientiks.add_orientiks_from_friends(db_session, recipient_user_id, amount)


async def spent(user_id: UUID, amount: int) -> None:
    async with async_session() as db_session:
        await orientiks.add_spent(db_session, user_id, amount)
