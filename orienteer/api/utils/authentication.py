import base64
import io
import urllib
from uuid import UUID

import qrcode
from fastapi import HTTPException

from orienteer.api.utils.discord import exchange_code, get_user_info
from orienteer.general.config import (AUTH_API_KEY, AUTH_REDIRECT_URI, BOT_ID, ROLES_PASSENGER, )
from orienteer.general.data.orienteer.services import discord_auth
from orienteer.general.data.ss14.services import player
from orienteer.general.utils import discord
from orienteer.general.utils.discord import set_role
from orienteer.general.utils.dtos import UserDTO


async def generate_link(user_id: UUID):
    state = urllib.parse.quote_plus(f"user_id={user_id}")
    return (f"https://discord.com/api/oauth2/authorize?client_id={BOT_ID}"
            f"&response_type=code"
            f"&state={state}"
            f"&redirect_uri={AUTH_REDIRECT_URI}"
            f"&scope=identify")


def generate_qr_code(url):
    qr_byte_array = io.BytesIO()
    image = qrcode.make(url)
    image.save(qr_byte_array)
    qr_byte_array.seek(0)
    qr_base64 = base64.b64encode(qr_byte_array.getvalue()).decode("utf-8")
    return qr_base64


async def generate_auth_data(user_id: UUID, key: str):
    if key != AUTH_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    auth_url = await generate_link(user_id)
    qrcode_data = generate_qr_code(auth_url)
    return {"Url": auth_url, "Qrcode": qrcode_data}


async def check_linked(user_dto: UserDTO):
    return {"IsLinked": await discord_auth.is_discord_linked(user_dto.user_id) and await discord.get_guild_profile(
        user_dto.discord_user_id) is not None}


async def discord_auth_redirect(code: str, state: str) -> dict:
    if not code:
        raise HTTPException(status_code=400, detail="Не удается получить код авторизации.")

    parsed_state = urllib.parse.parse_qs(state)
    user_id = UUID(parsed_state.get("user_id", [None])[0])

    if not user_id:
        raise HTTPException(status_code=400, detail="Не удалось получить идентификатор пользователя.")

    data = await exchange_code(code)

    if not data or "access_token" not in data:
        raise HTTPException(status_code=400, detail="Не удалось получить токен доступа.")

    token = data["access_token"]
    user_info = await get_user_info(token)
    user_name = await player.get_ckey(user_id)

    if user_name is None:
        raise HTTPException(status_code=400,
            detail="Аккаунт SS14, который вы пытаетесь верифицировать не существует.", )

    if await discord_auth.is_discord_linked(user_id):
        raise HTTPException(status_code=400, detail="Аккаунт SS14 уже подтвержден.")

    discord_user_id = int(user_info["id"])

    linked_user_id = await discord_auth.get_user_id_by_discord_user_id(discord_user_id)
    if linked_user_id is not None:
        raise HTTPException(status_code=400, detail=f"Дискорд аккаунт уже связан с пользователем "
                                                    f"{await player.get_ckey(linked_user_id)}.", )

    if await discord.get_guild_profile(discord_user_id) is None:
        raise HTTPException(status_code=400, detail=f"Вы не являетесь участником Discord сервера проекта", )

    await discord_auth.link_discord(user_id, discord_user_id, user_info["username"])
    await set_role(discord_user_id, ROLES_PASSENGER)

    return {"discord_name": user_info["username"], "user_name": user_name}
