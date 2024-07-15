import grequests
from orienteer.config import Bot


async def add_role(user_id: int, role_id: int):
    url = f'https://discord.com/api/v10/guilds/1075005001035943967/members/{
        user_id}/roles/{role_id}'

    headers = {
        'Authorization': f'Bot {Bot.TOKEN}',
        'Content-Type': 'application/json'
    }

    response = grequests.put(url, headers=headers)
    return response.status_code
