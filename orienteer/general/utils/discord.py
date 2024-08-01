from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from disnake import Webhook, Embed

from orienteer.general.config import BOT_TOKEN


async def add_role(user_id: int, role_id: int):
    url = f'https://discord.com/api/v10/guilds/1075005001035943967/members/{user_id}/roles/{role_id}'

    headers = {'Authorization': f'Bot {BOT_TOKEN}', 'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            return response.status


async def send_discord_message(webhook_url: str, username: str, title: str, description: str, color: int,
                               timestamp: datetime = None, image_url: str = None, message_id: int = None) -> bool:
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        if message_id:
            embed = Embed(title=title, description=description, color=color, timestamp=timestamp)
            embed.set_image(image_url)
            try:
                await webhook.edit_message(message_id, embed=embed)
            except ClientConnectorError:
                return False
            return True
        else:
            embed = Embed(title=title, description=description, color=color, timestamp=timestamp)
            embed.set_image(image_url)
            try:
                await webhook.send(username=username, embed=embed)
            except ClientConnectorError:
                return False
            return True
