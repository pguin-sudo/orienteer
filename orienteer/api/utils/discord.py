import aiohttp

from orienteer.general.config import AUTH_CLIENT_SECRET, AUTH_REDIRECT_URI, BOT_ID


async def exchange_code(code):
    data = {
        "client_id": BOT_ID,
        "client_secret": AUTH_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": AUTH_REDIRECT_URI,
        "scope": "identify",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token", data=data, headers=headers
        ) as response:
            return await response.json()


async def get_user_info(token):
    headers = {"authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://discord.com/api/v10/users/@me", headers=headers
        ) as response:
            return await response.json()
