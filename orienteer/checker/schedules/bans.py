from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from orienteer.general.config import WEBHOOKS_BANS
from orienteer.general.data.orienteer.services import orientiks, sent_bans
from orienteer.general.data.ss14.services import bans, player
from orienteer.general.formatting.playtime import get_job_group_and_name
from orienteer.general.formatting.time import get_formatted_datetime
from orienteer.general.utils.calculations import calculate_fine
from orienteer.general.utils.discord import send_discord_message

USERNAME = 'Каратель сервера Amadis'
REASON = 'Превышение нижнего порога штрафов'


async def _ban_if_fine_limit(user_id: UUID, reason: str):
    if await orientiks.get_balance(user_id) < -500 and reason != REASON:
        await bans.add_ban(user_id, REASON)


async def check_bans():
    last_sent_ban_id = await sent_bans.get_last_sent_ban_id()

    new_bans = await bans.get_all_bans_after(last_sent_ban_id)

    for ban in new_bans:
        server_ban_id = ban['server_ban_id']
        player_user_id = ban['player_user_id']
        ban_time = ban['ban_time']
        expiration_time = ban['expiration_time']
        reason = ban['reason']
        banning_admin = ban['banning_admin']

        await _ban_if_fine_limit(user_id=player_user_id, reason=reason)

        admin_name = await player.get_ckey(banning_admin) if banning_admin else 'Неизвестно'
        player_name = await player.get_ckey(player_user_id) if player_user_id else 'Неизвестно'

        if expiration_time is None:
            expiration_time_str = 'Никогда'
            embed_title = f'**Пермабан** {server_ban_id}'
            color = int('e84f4f', 16)
            fine = '∞'
        else:
            expiration_time_str = get_formatted_datetime(expiration_time)
            embed_title = f'**Бан** {server_ban_id}'
            color = int('5c85d6', 16)
            fine = calculate_fine(expiration_time - ban_time)

        embed_desc = f'**Нарушитель:** {player_name}\n'
        embed_desc += f'**Администратор:** {admin_name}\n\n'
        embed_desc += f'**Время получения:** {get_formatted_datetime(ban_time)}\n'
        embed_desc += f'**Время снятия:** {expiration_time_str}\n'
        embed_desc += f'**Штраф:** {fine} <:orienta:1250903370894671963>\n\n'
        embed_desc += f'**Причина:** {reason}\n'

        await send_discord_message(WEBHOOKS_BANS, USERNAME, embed_title, embed_desc, color)

        await sent_bans.set_last_sent_ban_id(server_ban_id)

        logger.info(f'New ban with ID: {server_ban_id}')


async def check_role_bans():
    last_sent_role_ban_id = await sent_bans.get_last_sent_role_ban_id()

    new_role_bans = await bans.get_all_role_bans_after(last_sent_role_ban_id)

    for role_ban in new_role_bans:
        server_role_ban_id = role_ban['server_role_ban_id']
        player_user_id = role_ban['player_user_id']
        ban_time = role_ban['ban_time']
        expiration_time = role_ban['expiration_time']
        reason = role_ban['reason']
        banning_admin = role_ban['banning_admin']
        role_id = role_ban['role_id']

        admin_name = await player.get_ckey(banning_admin) if banning_admin else 'Неизвестно'
        player_name = await player.get_ckey(player_user_id) if player_user_id else 'Неизвестно'

        if expiration_time is None:
            expiration_time = 'Никогда'
            color = int('d183ad', 16)
        else:
            expiration_time = get_formatted_datetime(expiration_time)
            color = int('cbc0ff', 16)

        job_description = get_job_group_and_name(str(role_id).replace(':', ''))[1]

        embed_title = f'**Ролебан** {server_role_ban_id}'
        embed_desc = f'**Нарушитель:** {player_name}\n'
        embed_desc += f'**Администратор:** {admin_name}\n\n'
        embed_desc += f'**Роль:** {job_description}\n\n'
        embed_desc += f'**Время получения:** {get_formatted_datetime(ban_time)}\n'
        embed_desc += f'**Время снятия:** {expiration_time}\n\n'
        embed_desc += f'**Причина:** {reason}\n'

        await send_discord_message(WEBHOOKS_BANS, USERNAME, embed_title, embed_desc, color)

        await sent_bans.set_last_sent_role_ban_id(server_role_ban_id)

        logger.info(f'New role_ban with ID: {server_role_ban_id}')


async def setup_bans_schedule(scheduler: AsyncIOScheduler):
    await check_bans()
    await check_role_bans()

    scheduler.add_job(check_bans, CronTrigger(minute='*'))
    scheduler.add_job(check_role_bans, CronTrigger(minute='*'))
