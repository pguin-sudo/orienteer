from ..database import database_helper
from ..repositories import sent_bans


async def get_last_sent_ban_id() -> int:
    async with database_helper.session_factory() as db_session:
        return await sent_bans.get_last_sent_ban_id(db_session)


async def get_last_sent_role_ban_id() -> int:
    async with database_helper.session_factory() as db_session:
        return await sent_bans.get_last_sent_role_ban_id(db_session)


async def set_last_sent_ban_id(id_: int) -> None:
    async with database_helper.session_factory() as db_session:
        await sent_bans.set_last_sent_ban_id(db_session, id_)


async def set_last_sent_role_ban_id(id_: int) -> None:
    async with database_helper.session_factory() as db_session:
        await sent_bans.set_last_sent_role_ban_id(db_session, id_)
