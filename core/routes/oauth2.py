from uuid import UUID

from flask import jsonify, render_template
import requests
import io
import base64
import urllib.parse
import qrcode

from core.config import OAuth2, Roles
from core.data import ss14
from core.info import tools


def exchange_code(code):
    response = requests.post('https://discord.com/api/oauth2/token', data={
        'client_id': OAuth2.CLIENT_ID,
        'client_secret': OAuth2.CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': OAuth2.REDIRECT_URI,
        'scope': 'identify',
    }, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    })
    return response.json()


def get_user_info(token):
    headers = {'authorization': f'Bearer {token}'}
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    return response.json()


def generate_link(user_id: UUID):
    state = urllib.parse.quote_plus(f'user_id={user_id}')
    return (f'https://discord.com/api/oauth2/authorize?client_id={OAuth2.CLIENT_ID}'
            f'&response_type=code'
            f'&state={state}'
            f'&redirect_uri={OAuth2.REDIRECT_URI}'
            f'&scope=identify')


def generate_qr_code(url):
    qr_byte_array = io.BytesIO()
    image = qrcode.make(url)
    image.save(qr_byte_array)
    qr_byte_array.seek(0)
    qr_base64 = base64.b64encode(qr_byte_array.getvalue()).decode('utf-8')
    return qr_base64


def generate_auth_data(user_id: UUID, key: str):
    if key != OAuth2.API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

    auth_url = generate_link(user_id)
    qrcode_data = generate_qr_code(auth_url)
    return jsonify({'Url': auth_url, 'Qrcode': qrcode_data})


async def check_linked(user_id: UUID):
    return jsonify({'IsLinked': await ss14.is_discord_linked(user_id)})


async def discord_auth_redirect(code: str, state):
    if code is None or not code:
        return render_template(f'error.html', message='Не удалось получить код доступа')

    parsed_state = urllib.parse.parse_qs(state)
    user_id = parsed_state.get('user_id', [None])[0]

    if user_id is None:
        return render_template(f'error.html', message='Не удалось получить идентификатор пользователя')

    data = exchange_code(code)

    if not data or 'access_token' not in data:
        return render_template(f'error.html', message='Не удалось получить токен доступа')

    token = data['access_token']
    user_info = get_user_info(token)
    print(user_info)
    user_name = await ss14.get_ckey(user_id)
    if user_name is None:
        return render_template(f'error.html', message='Неверный идентификатор пользователя')

    if await ss14.is_discord_linked(user_id):
        return render_template(f'error.html', message='Аккаунт уже был верифицирован')

    discord_user_id = int(user_info['id'])
    await ss14.link_discord(user_id, discord_user_id, user_info['username'])

    await tools.add_role(discord_user_id, Roles.PASSENGER)

    return render_template(f'success.html', discord_name=user_info['username'], user_name=user_name)
