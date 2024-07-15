from datetime import datetime, timezone, timedelta
from uuid import UUID

from ..repositories import bans
from orienteer.general.data.ss14.services.player import get_ckey

from orienteer.general.formatting.time import get_formatted_datetime

from orienteer.general.utils.calculations import calculate_fine


async def get_formatted_bans_and_total_stats(user_id: UUID) -> tuple[tuple[str, str]]:
    all_bans = await bans.get_bans(user_id)
    formatted = []
    total_time = timedelta(minutes=0)
    total_fine = 0
    for ban in all_bans:
        server_ban_id = ban['server_ban_id']
        ban_time = ban['ban_time']
        expiration_time = ban['expiration_time']
        reason = ban['reason']
        banningadmin = ban['banning_admin']

        admin_name = await get_ckey(banningadmin) if banningadmin is not None else 'Неизвестно'
        bantime_str = get_formatted_datetime(ban_time)

        if expiration_time is None:
            expiration_time_str = 'Никогда'
            fine = '∞'
        else:
            expiration_time_str = get_formatted_datetime(expiration_time)
            ban_time = expiration_time - ban_time
            total_time += ban_time
            fine = await calculate_fine(ban_time)
            total_fine += fine

        title = f'**Бан** {server_ban_id}'
        description = f'**Администратор:** {admin_name}\n'
        description += f'**Время получения:** {bantime_str}\n'
        description += f'**Время снятия:** {expiration_time_str}\n'
        description += f'**Штраф:** {
            fine} <:orienta:1250903370894671963>\'s\n'
        description += f'**Причина:** {reason}\n'

        formatted.append((title, description))
    return formatted, total_time, total_fine


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
        if ban['expirationtime'] is None:
            return 2
        if ban['expirationtime'] > datetime.now(timezone.utc):
            return 1
    else:
        return 0
