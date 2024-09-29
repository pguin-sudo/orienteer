import math
from datetime import datetime
from typing import Any
from uuid import UUID

from aiocache import cached
from aiocache.serializers import PickleSerializer

from orienteer.general.config import ORIENTIKS_MARGIN, ORIENTIKS_PRICE_COEFFICIENT
from orienteer.general.utils import discord
from orienteer.general.utils.dtos import UserDTO
from ..database import database_helper
from ..models.orientiks_cached_info import OrientiksCachedInfo
from ..models.transactions import TransactionType
from ..repositories import transactions, role_time_coefficients
from ...ss14.services import bans, player

PRICE = 2  # for 1 hour
PRICE_FOR_INIT = 1.3  # was 1.95


async def get_balance(user_id: UUID) -> int:
    async with database_helper.session_factory() as db_session:
        balance = await transactions.get_balance(db_session, user_id=user_id)

    fine = await bans.get_fine(user_id=user_id)

    return int(balance - fine)


async def do_transfer(sender_user_id: UUID, recipient_user_id: UUID, amount: int) -> None:
    async with database_helper.session_factory() as db_session:
        await transactions.add_transaction(db_session, sender_user_id, -amount, TransactionType.Transfer,
                                           f'Transfer to "{await player.get_ckey(recipient_user_id)}"', )
        await transactions.add_transaction(db_session, recipient_user_id, amount, TransactionType.Transfer,
                                           f'Transfer from "{await player.get_ckey(recipient_user_id)}"', )


async def add_orientiks_from_playtime(user_dto: UserDTO, minutes: int) -> None:
    async with database_helper.session_factory() as db_session:
        if user_dto is None:
            return

        profile = await discord.get_guild_profile(user_dto.discord_user_id)
        role_ids = (int(role_id) for role_id in profile["roles"]) if profile else (0,)
        coefficient = await role_time_coefficients.get_coefficients_by_roles(db_session, role_ids)

        if coefficient == 0:
            return

        await transactions.add_transaction(db_session, user_dto.user_id, minutes * coefficient,
                                           TransactionType.Playtime, )


async def add_orientiks_from_boosty(user_id: UUID, amount: int) -> None:
    async with database_helper.session_factory() as db_session:
        await transactions.add_transaction(db_session, user_id, amount, TransactionType.Boosty)


async def add_orientiks_from_tip(user_id: UUID, amount: int, name: str) -> None:
    async with database_helper.session_factory() as db_session:
        await transactions.add_transaction(db_session, user_id, amount, TransactionType.Tip, name)


async def add_orientiks_from_other(user_id: UUID, amount: int, name: str) -> None:
    async with database_helper.session_factory() as db_session:
        await transactions.add_transaction(db_session, user_id, amount, TransactionType.Other, name)


async def spend(user_id: UUID, amount: int) -> None:
    async with database_helper.session_factory() as db_session:
        await transactions.add_transaction(db_session, user_id, -amount)


# @deprecated
async def get_cached_info_range(start: datetime | None = None, end: datetime | None = None) -> tuple[
    OrientiksCachedInfo, ...]:
    async with database_helper.session_factory() as db_session:
        return await transactions.get_cached_info_range(db_session)


# @deprecated
async def get_cached_info_one(timestamp: datetime | None = None) -> OrientiksCachedInfo:
    timestamp = timestamp or datetime.now()
    async with database_helper.session_factory() as db_session:
        return await transactions.get_cached_info_one(db_session, timestamp)


# @deprecated
async def get_price(buy: bool, timestamp: datetime | None = None) -> float:
    timestamp = timestamp or datetime.now()
    async with database_helper.session_factory() as db_session:
        cached_info = await transactions.get_cached_info_one(db_session, timestamp)

        numerator = math.log(cached_info.total_fine + cached_info.total_spent + 1)
        denominator = math.log(
            cached_info.total_from_time - cached_info.total_time_balancing + cached_info.total_sponsorship + 1)

        clean_price = (numerator / denominator) * ORIENTIKS_PRICE_COEFFICIENT

        price = (clean_price * (1 + ORIENTIKS_MARGIN) if buy else clean_price * (1 - ORIENTIKS_MARGIN))
        return round(price, 2)


# @deprecated
@cached(ttl=3600, serializer=PickleSerializer())
async def get_leaderboard(depth: int = 27) -> tuple[tuple[UserDTO, Any], ...]:
    leaderboard = []

    async with database_helper.session_factory() as db_session:
        async for user_id in player.all_user_ids_generator():
            if await bans.get_last_ban_status(user_id) == 2:
                continue

            leaderboard.append((await UserDTO.from_user_id(user_id), await get_balance(user_id)))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    return tuple(leaderboard[:depth])
