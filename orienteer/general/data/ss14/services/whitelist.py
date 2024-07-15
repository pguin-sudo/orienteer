from uuid import UUID

from ..repositories import whitelist


async def check_whitelist(user_id: UUID) -> bool:
    return await whitelist.check_whitelist(user_id)


async def delete_from_whitelist(user_id: UUID) -> str | None:
    return await whitelist.delete_from_whitelist(user_id)


async def add_to_whitelist(user_id: UUID) -> str | None:
    return await whitelist.add_to_whitelist(user_id)
