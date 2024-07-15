from uuid import UUID
from ..repositories import player


async def get_user_id(nickname: str) -> UUID | None:
    return await player.get_user_id(nickname)


async def get_ckey(user_id: UUID) -> str | None:
    return await player.get_ckey(user_id)


async def get_discord_user_id_by_user_id(user_id: UUID) -> str | None:
    return await player.get_discord_user_id_by_user_id(user_id)


async def get_user_id_by_discord_user_id(discord_user_id: int) -> UUID | None:
    return await player.get_user_id_by_discord_user_id(discord_user_id)
