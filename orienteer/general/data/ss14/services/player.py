from uuid import UUID
from ..repositories import player


async def get_user_id(nickname: str) -> UUID | None:
    return await player.get_user_id(nickname)


async def get_ckey(user_id: UUID) -> str | None:
    return await player.get_ckey(user_id)
