from uuid import UUID

from ..repositories import whitelist


async def check_whitelist(user_id: UUID) -> bool:
    return await whitelist.check(user_id)


async def delete_from_whitelist(user_id: UUID) -> str | None:
    if not await whitelist.check(user_id):
        return await whitelist.delete_user(user_id)
    else:
        return None


async def add_to_whitelist(user_id: UUID) -> str | None:
    if not await whitelist.check(user_id):
        return await whitelist.add_user(user_id)
    else:
        return None
