import asyncio
import time

import requests
import json

from core.checker import bans
from core.info import commands
from core.data import ss14, discord_time, formulas

from core.config.main import Webhooks, Cache


def send_discord_message(message, username, embed_description, embed_title, webhook, color):
    data = {
        'username': username,
        'content': message,
        'embeds': [
            {
                'title': embed_title,
                'description': embed_description,
                'color': color
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    requests.post(webhook, data=json.dumps(data), headers=headers)


async def check_bans():
    with open(Cache.BANS_LAST_ID, 'r') as file:
        last_processed_id = int(file.read())

    new_bans = await ss14.get_all_bans_after(last_processed_id)

    for ban in new_bans:
        server_ban_id = ban['server_ban_id']
        player_user_id = ban['player_user_id']
        ban_time = ban['ban_time']
        expiration_time = ban['expiration_time']
        reason = ban['reason']
        banning_admin = ban['banning_admin']

        await bans.ban_if_fine_limit(user_id=player_user_id, reason=reason)

        admin_name = await ss14.get_ckey(banning_admin) if banning_admin else 'Неизвестно'
        player_name = await ss14.get_ckey(player_user_id) if player_user_id else 'Неизвестно'

        if expiration_time is None:
            expiration_time_str = "Никогда"
            embed_title = f"**Пермабан** {server_ban_id}"
            color = 15224655
            fine = "∞"
        else:
            expiration_time_str = await discord_time.get_discord_datetime_tag(expiration_time)
            embed_title = f"**Бан** {server_ban_id}"
            color = 6063574
            fine = await formulas.calculate_fine(expiration_time - ban_time)

        username = "Каратель сервера Amadis"
        message = ""
        embed_disc = f"**Нарушитель:** {player_name}\n"
        embed_disc += f"**Администратор:** {admin_name}\n\n"
        embed_disc += f"**Время получения:** {await discord_time.get_discord_datetime_tag(ban_time)}\n"
        embed_disc += f"**Время снятия:** {expiration_time_str}\n"
        embed_disc += f"**Штраф:** {fine} <:orienta:1250903370894671963>\'s\n\n"
        embed_disc += f"**Причина:** {reason}\n"

        send_discord_message(message, username, embed_disc, embed_title, Webhooks.BANS, color)

        with open(Cache.BANS_LAST_ID, 'w') as file:
            file.write(str(server_ban_id))

        print('New ban with ID: ', server_ban_id)


async def check_rolebans():
    with open(Cache.ROLEBANS_LAST_ID, 'r') as file:
        last_processed_id = int(file.read())

    new_bans = await ss14.get_all_rolebans_after(last_processed_id)

    for ban in new_bans:
        server_ban_id = ban['server_role_ban_id']
        player_user_id = ban['player_user_id']
        ban_time = ban['ban_time']
        expiration_time = ban['expiration_time']
        reason = ban['reason']
        banning_admin = ban['banning_admin']
        role_id = ban['role_id']

        admin_name = await ss14.get_ckey(banning_admin) if banning_admin else 'Неизвестно'
        player_name = await ss14.get_ckey(player_user_id) if player_user_id else 'Неизвестно'

        if expiration_time is None:
            expiration_time = "Никогда"
            color = 13730733
        else:
            expiration_time = await discord_time.get_discord_datetime_tag(expiration_time)
            color = 16761035

        job_description = commands.get_job_description(str(role_id).replace(':', ''))[1]

        username = "Каратель сервера Amadis"
        message = ""
        embed_title = f"**Ролебан** {server_ban_id}"
        embed_disc = f"**Нарушитель:** {player_name}\n"
        embed_disc += f"**Администратор:** {admin_name}\n\n"
        embed_disc += f"**Роль:** {job_description}\n\n"
        embed_disc += f"**Время получения:** {await discord_time.get_discord_datetime_tag(ban_time)}\n"
        embed_disc += f"**Время снятия:** {expiration_time}\n\n"
        embed_disc += f"**Причина:** {reason}\n"

        send_discord_message(message, username, embed_disc, embed_title, Webhooks.ROLEBANS, color)

        with open(Cache.ROLEBANS_LAST_ID, 'w') as file:
            file.write(str(server_ban_id))

        print('New roleban with ID: ', server_ban_id)


if __name__ == '__main__':
    while True:
        asyncio.run(check_bans())
        asyncio.run(check_rolebans())
        time.sleep(60 * 5)
