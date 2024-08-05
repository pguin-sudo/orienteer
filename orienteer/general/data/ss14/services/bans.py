from datetime import datetime, timezone, timedelta
from uuid import UUID

from orienteer.general.data.ss14.services.player import get_ckey
from orienteer.general.formatting.time import get_formatted_datetime
from orienteer.general.utils.calculations import calculate_fine
from ..repositories import bans


async def get_formatted_bans_and_total_stats(user_id: UUID) -> tuple[list[tuple[str, str]], timedelta, int]:
    all_bans = await bans.get_bans(user_id)
    formatted = []
    total_time = timedelta(minutes=0)
    total_fine = 0
    for ban in all_bans:
        server_ban_id = ban['server_ban_id']
        ban_time = ban['ban_time']
        expiration_time = ban['expiration_time']
        reason = ban['reason']
        banning_admin = ban['banning_admin']

        admin_name = await get_ckey(banning_admin) if banning_admin is not None else 'Неизвестно'
        bantime_str = get_formatted_datetime(ban_time)

        if expiration_time is None:
            expiration_time_str = 'Никогда'
            fine = '∞'
        else:
            expiration_time_str = get_formatted_datetime(expiration_time)
            ban_time = expiration_time - ban_time
            total_time += ban_time
            fine = calculate_fine(ban_time)
            total_fine += fine

        title = f'**Бан** {server_ban_id}'
        description = f'**Администратор:** {admin_name}\n'
        description += f'**Время получения:** {bantime_str}\n'
        description += f'**Время снятия:** {expiration_time_str}\n'
        description += f'**Штраф:** {fine} <:orienta:1250903370894671963>\'s\n'
        description += f'**Причина:** {reason}\n'

        formatted.append((title, description))
    return formatted, total_time, total_fine


async def get_last_ban(user_id: UUID) -> dict | None:
    return await bans.get_last_ban(user_id)


async def get_last_ban_status(user_id: UUID) -> int:
    ban = await bans.get_last_ban(user_id)

    """
    0 - Без банов
    1 - Временный
    2 - Пермач
    """

    if ban is None:
        return 0
    elif ban:
        if ban['expiration_time'] is None:
            return 2
        if ban['expiration_time'] > datetime.now(timezone.utc):
            return 1

    return 0


async def pardon_last_ban(user_id: UUID):
    last_ban = await bans.get_last_ban(user_id)
    if last_ban is not None:
        await bans.pardon_ban(last_ban['server_ban_id'])


async def get_all_bans_after(ban_id) -> tuple[dict]:
    return await bans.get_all_bans_after(ban_id)


async def get_all_role_bans_after(ban_id) -> tuple[dict]:
    return await bans.get_all_role_bans_after(ban_id)


async def add_ban(user_id: UUID, reason: str):
    return await bans.add_ban(user_id, reason)


async def get_fine(user_id: UUID) -> int:
    return int(sum(
        [calculate_fine(ban['expiration_time'] - ban['ban_time']) for ban in await bans.get_bans(user_id=user_id) if
         ban['expiration_time'] is not None]))
