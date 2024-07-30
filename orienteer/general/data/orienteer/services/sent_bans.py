
from orienteer.general.data.orienteer.repositories import sent_bans
from ..database import async_session


async def get_last_sent_ban_id() -> int:
    async with async_session() as db_session:
        return await sent_bans.get_last_sent_ban_id(db_session)


async def get_last_sent_role_ban_id() -> int:
    async with async_session() as db_session:
        return await sent_bans.get_last_sent_role_ban_id(db_session)


async def set_last_sent_ban_id(id: int) -> None:
    async with async_session() as db_session:
        await sent_bans.set_last_sent_ban_id(db_session, id)


async def set_last_sent_role_ban_id(id: int) -> None:
    async with async_session() as db_session:
        await sent_bans.set_last_sent_role_ban_id(db_session, id)
