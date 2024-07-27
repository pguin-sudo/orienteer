
import asyncio
from datetime import datetime, timezone
from loguru import logger

from orienteer.general.config.main import WEBHOOKS_BANS
from orienteer.general.data.orienteer.services import sent_bans
from orienteer.general.data.ss14.services import bans, player
from orienteer.general.formatting.playtime import get_job_group_and_name
from orienteer.general.formatting.time import get_formatted_datetime
from orienteer.general.utils.calculations import calculate_fine
from orienteer.general.utils.discord import send_discord_message


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

        await bans.ban_if_fine_limit(user_id=player_user_id, reason=reason)

        admin_name = await player.get_ckey(banning_admin) if banning_admin else 'Неизвестно'
        player_name = await player.get_ckey(player_user_id) if player_user_id else 'Неизвестно'

        if expiration_time is None:
            expiration_time_str = "Никогда"
            embed_title = f"**Пермабан** {server_ban_id}"
            color = 15224655
            fine = "∞"
        else:
            expiration_time_str = get_formatted_datetime(expiration_time)
            embed_title = f"**Бан** {server_ban_id}"
            color = 6063574
            fine = calculate_fine(expiration_time - ban_time)

        username = "Каратель сервера Amadis"
        message = ""
        embed_disc = f"**Нарушитель:** {player_name}\n"
        embed_disc += f"**Администратор:** {admin_name}\n\n"
        embed_disc += f"**Время получения:** {
            get_formatted_datetime(ban_time)}\n"
        embed_disc += f"**Время снятия:** {expiration_time_str}\n"
        embed_disc += f"**Штраф:** {fine} <:orienta:1250903370894671963>\'s\n\n"
        embed_disc += f"**Причина:** {reason}\n"

        if not await send_discord_message(message, username, embed_disc,
                                          embed_title, WEBHOOKS_BANS, color):
            return

        sent_bans.set_last_sent_ban_id(server_ban_id)

        logger('New ban with ID: ', server_ban_id)


async def check_rolebans():
    last_sent_roleban_id = await sent_bans.get_last_sent_roleban_id()

    new_rolebans = await bans.get_all_rolebans_after(last_sent_roleban_id)

    for roleban in new_rolebans:
        server_roleban_id = roleban['server_role_ban_id']
        player_user_id = roleban['player_user_id']
        ban_time = roleban['ban_time']
        expiration_time = roleban['expiration_time']
        reason = roleban['reason']
        banning_admin = roleban['banning_admin']
        role_id = roleban['role_id']

        admin_name = await player.get_ckey(banning_admin) if banning_admin else 'Неизвестно'
        player_name = await player.get_ckey(player_user_id) if player_user_id else 'Неизвестно'

        if expiration_time is None:
            expiration_time = "Никогда"
            color = 13730733
        else:
            expiration_time = get_formatted_datetime(expiration_time)
            color = 16761035

        job_description = get_job_group_and_name(
            str(role_id).replace(':', ''))[1]

        username = "Каратель сервера Amadis"
        message = ""
        embed_title = f"**Ролебан** {server_roleban_id}"
        embed_disc = f"**Нарушитель:** {player_name}\n"
        embed_disc += f"**Администратор:** {admin_name}\n\n"
        embed_disc += f"**Роль:** {job_description}\n\n"
        embed_disc += f"**Время получения:** {
            get_formatted_datetime(ban_time)}\n"
        embed_disc += f"**Время снятия:** {expiration_time}\n\n"
        embed_disc += f"**Причина:** {reason}\n"

        send_discord_message(message, username, embed_disc,
                             embed_title, WEBHOOKS_BANS, color)

        if not await send_discord_message(message, username, embed_disc,
                                          embed_title, WEBHOOKS_BANS, color):
            return

        sent_bans.set_last_sent_roleban_id(server_roleban_id)

        logger('New roleban with ID: ', server_roleban_id)


async def schedule_bans():
    await asyncio.sleep((5-(datetime.now(timezone.utc).minute % 5))*60)
    while True:
        await check_bans()
        await check_rolebans()
        await asyncio.sleep(60*5)
