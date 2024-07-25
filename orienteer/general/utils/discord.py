import aiohttp
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
