from uuid import UUID

from ..database import async_session
from ..repositories import orientiks
from ...ss14.services import bans, playtime

price = 2
price_for_init = 1.3  # was 1.95


async def _init_balance(user_id: UUID) -> None:
    overall = await playtime.get_overall(user_id)
    async with async_session() as db_session:
        await orientiks.add_time_balancing(db_session, user_id, int(overall.total_seconds() // 3600 * price_for_init))


async def get_balance(user_id: UUID) -> int:
    overall = await playtime.get_overall(user_id)

    if overall is None:
        return 0

    async with async_session() as db_session:
        raw_info = await orientiks.get_balance_raw_info(db_session, user_id=user_id)
        if raw_info is None:
            await _init_balance(user_id)
            raw_info = await orientiks.get_balance_raw_info(db_session, user_id=user_id)

    fine = await bans.get_fine(user_id=user_id)

    return int(
        overall.total_seconds() // 3600 * price
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


async def add_orientiks_from_sponsorship(user_id: UUID, amount: int) -> None:
    async with async_session() as db_session:
        await orientiks.add_orientiks_from_sponsorship(db_session, user_id, amount)


async def spent(user_id: UUID, amount: int) -> None:
    async with async_session() as db_session:
        await orientiks.add_spent(db_session, user_id, amount)


async def add_time_balancing(user_id: UUID, minutes: int) -> None:
    async with async_session() as db_session:
        await orientiks.add_time_balancing(db_session, user_id, minutes)

