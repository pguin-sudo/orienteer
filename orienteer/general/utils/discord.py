from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ServerDisconnectedError
from disnake import Webhook, Embed

from orienteer.general.config.main import BOT_TOKEN


async def set_role(discord_user_id: int, role_id: int, remove: bool = False):
    url = f"https://discord.com/api/v10/guilds/1075005001035943967/members/{discord_user_id}/roles/{role_id}"

    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        if remove:
            async with session.delete(url, headers=headers) as response:
                if response.status // 100 == 4:
                    pass
                    # raise ServerDisconnectedError

        else:
            async with session.put(url, headers=headers) as response:
                if response.status // 100 == 4:
                    pass
                    # raise ServerDisconnectedError


async def get_guild_profile(
    discord_user_id: int, server_id: int = 1075005001035943967
) -> dict | None:
    url = f"https://discord.com/api/v10/guilds/{server_id}/members/{discord_user_id}"

    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status // 100 != 4:
                data = await response.json()
                if data.get("message", None) == "Unknown member":
                    return None
                return data
            else:
                return None


async def send_discord_message(
    webhook_url: str,
    username: str,
    title: str,
    description: str,
    color: int,
    timestamp: datetime | None = None,
    image_url: str | None = None,
    message_id: int | None = None,
) -> bool:
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        if message_id:
            embed = Embed(
                title=title, description=description, color=color, timestamp=timestamp
            )
            embed.set_image(image_url)
            try:
                await webhook.edit_message(message_id, embed=embed)
            except ClientConnectorError:
                return False
            return True
        else:
            embed = Embed(
                title=title, description=description, color=color, timestamp=timestamp
            )
            embed.set_image(image_url)
            try:
                await webhook.send(username=username, embed=embed)
            except ClientConnectorError:
                return False
            return True
