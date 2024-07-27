import json
import aiohttp
from loguru import logger
from orienteer.general.config.local import BOT_TOKEN


async def add_role(user_id: int, role_id: int):
    url = f'https://discord.com/api/v10/guilds/1075005001035943967/members/{
        user_id}/roles/{role_id}'

    headers = {
        'Authorization': f'Bot {BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            return response.status


async def send_discord_message(message, username, embed_description, embed_title, webhook, color) -> bool:
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

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook, data=json.dumps(data), headers=headers) as response:
            if response.status == 200:
                return True
    logger.error('Can\'t send message')
    return False
