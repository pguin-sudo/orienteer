import base64
import io
from uuid import UUID

import qrcode
import urllib
from fastapi import HTTPException

from orienteer.api.utils.discord import exchange_code, get_user_info
from orienteer.general.data.orienteer.services import discord_auth
from orienteer.general.data.ss14.services import player
from orienteer.general.utils.discord import add_role

from orienteer.general.config.local import AUTH_API_KEY, AUTH_REDIRECT_URI, BOT_ID, ROLES_PASSENGER


async def generate_link(user_id: UUID):
    state = urllib.parse.quote_plus(f'user_id={user_id}')
    return (f'https://discord.com/api/oauth2/authorize?client_id={BOT_ID}'
            f'&response_type=code'
            f'&state={state}'
            f'&redirect_uri={AUTH_REDIRECT_URI}'
            f'&scope=identify')


def generate_qr_code(url):
    qr_byte_array = io.BytesIO()
    image = qrcode.make(url)
    image.save(qr_byte_array)
    qr_byte_array.seek(0)
    qr_base64 = base64.b64encode(qr_byte_array.getvalue()).decode('utf-8')
    return qr_base64


async def generate_auth_data(user_id: UUID, key: str):
    if key != AUTH_API_KEY:
        raise HTTPException(status_code=401, detail='Unauthorized')

    auth_url = generate_link(user_id)
    qrcode_data = generate_qr_code(auth_url)
    return {'Url': auth_url, 'Qrcode': qrcode_data}


async def check_linked(user_id: UUID):
    is_linked = await discord_auth.is_discord_linked(user_id)
    return {'IsLinked': is_linked}


async def discord_auth_redirect(code: str, state: str) -> dict:
    if not code:
        raise HTTPException(
            status_code=400, detail='Не удается получить код авторизации.')

    parsed_state = urllib.parse.parse_qs(state)
    user_id = parsed_state.get('user_id', [None])[0]

    if not user_id:
        raise HTTPException(
            status_code=400, detail='Не удалось получить идентификатор пользователя.')

    data = await exchange_code(code)

    if not data or 'access_token' not in data:
        raise HTTPException(
            status_code=400, detail='Не удалось получить токен доступа.')

    token = data['access_token']
    user_info = await get_user_info(token)
    user_name = await player.get_ckey(user_id)

    if user_name is None:
        raise HTTPException(
            status_code=400, detail='Неверный идентификатор пользователя.')

    if await discord_auth.is_discord_linked(user_id):
        raise HTTPException(status_code=400, detail='Аккаунт уже подтвержден.')

    discord_user_id = int(user_info['id'])
    await discord_auth.link_discord(user_id, discord_user_id, user_info['username'])
    await add_role(discord_user_id, ROLES_PASSENGER)

    return {'discord_name': user_info['username'], 'user_name': user_name}
