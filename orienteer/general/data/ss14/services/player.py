from typing import AsyncGenerator
from uuid import UUID

from aiocache import cached
from aiocache.serializers import PickleSerializer

from ..repositories import player


async def get_user_id(ckey: str) -> UUID | None:
    return await player.get_user_id(ckey)


async def get_user_id_nocased(ckey: str) -> tuple[UUID | None, str]:
    """
    Возвращает user_id и ckey игрока с ckey, а если без учета регистра есть только 1 игрок - его user_id
    """
    return await player.get_user_id_nocased(ckey)


async def get_ckey(user_id: UUID) -> str | None:
    return await player.get_ckey(user_id)


def all_user_ids_generator() -> AsyncGenerator[UUID, None]:
    return player.all_user_ids_generator()


@cached(ttl=60, serializer=PickleSerializer())
async def contains_in_ckeys(user_input: str) -> list[str]:
    ckeys = []
    async for ckey in player.all_ckey_generator():
        if user_input.lower() in ckey.lower():
            ckeys.append(ckey)
            if len(ckeys) >= 20:
                break
    return ckeys
