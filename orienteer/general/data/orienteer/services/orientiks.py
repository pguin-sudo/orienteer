from uuid import UUID

from ..database import async_session
from ..models.orientiks import Orientiks
from ..models.orientiks_cached_info import OrientiksCachedInfo
from ..repositories import orientiks, orientiks_cached_info
from ...ss14.services import bans, playtime, player

PRICE = 2  # for 1 hour
PRICE_FOR_INIT = 1.3  # was 1.95


def _calculate_balance(overall, raw_info: Orientiks, fine) -> int:
    return int(
        overall.total_seconds() // 3600 * PRICE + raw_info.sponsorship + raw_info.friends + raw_info.pardons - raw_info.time_balancing - raw_info.spent - fine)


async def _init_balance(user_id: UUID) -> None:
    overall = await playtime.get_overall(user_id)
    async with async_session() as db_session:
        await orientiks.add_time_balancing(db_session, user_id, int(overall.total_seconds() // 3600 * PRICE_FOR_INIT))


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

    return _calculate_balance(overall, raw_info, fine)


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


async def add_calculated_cached_info() -> OrientiksCachedInfo:
    # Initialize the info object with default values
    info = OrientiksCachedInfo(total_sponsorship=0, total_friends=0, total_pardons=0, total_time_balancing=0,
                               total_spent=0, total_fine=0, total_from_time=0)

    async with async_session() as db_session:
        # Iterate over all user IDs
        async for user_id in player.all_user_ids_generator():
            # Fetch the overall playtime for the user
            overall = await playtime.get_overall(user_id)
            if overall is None:
                continue

            # Fetch raw balance info
            raw_info = await orientiks.get_balance_raw_info(db_session, user_id=user_id)
            if raw_info is None:
                # Initialize balance if info is not available
                await _init_balance(user_id)
                raw_info = await orientiks.get_balance_raw_info(db_session, user_id=user_id)

            # Fetch any fines the user might have
            fine = await bans.get_fine(user_id=user_id)

            # Accumulate totals
            info.total_sponsorship += raw_info.sponsorship
            info.total_friends += raw_info.friends
            info.total_pardons += raw_info.pardons
            info.total_time_balancing += raw_info.time_balancing
            info.total_spent += raw_info.spent
            info.total_fine += fine
            info.total_from_time += int(overall.total_seconds() // 3600 * PRICE)

    # Update the cached information in the database
    async with async_session() as db_session:
        await orientiks_cached_info.add_cached_info(db_session, info)

    return info


async def get_all_cached_info() -> tuple[OrientiksCachedInfo, ...]:
    async with async_session() as db_session:
        return await orientiks_cached_info.get_all_cached_info(db_session)


async def get_last_cached_info() -> OrientiksCachedInfo:
    async with async_session() as db_session:
        return await orientiks_cached_info.get_last_cached_info(db_session)
