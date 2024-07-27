from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orienteer.general.data.orienteer.models.sent_bans import SentBan


async def get_last_sent_ban_id(db_session: AsyncSession) -> int:
    result = await db_session.execute(
        select(SentBan.last_sent_ban_id).order_by(SentBan.id.desc()).limit(1)
    )
    return result.scalar_one_or_none() or 0


async def get_last_sent_roleban_id(db_session: AsyncSession) -> int:
    result = await db_session.execute(
        select(SentBan.last_sent_roleban_id).order_by(
            SentBan.id.desc()).limit(1)
    )
    return result.scalar_one_or_none() or 0


async def set_last_sent_ban_id(db_session: AsyncSession, id: int) -> None:
    await db_session.execute(
        update(SentBan).values(last_sent_ban_id=id)
    )
    await db_session.commit()


async def set_last_sent_roleban_id(db_session: AsyncSession, id: int) -> None:
    await db_session.execute(
        update(SentBan).values(last_sent_roleban_id=id)
    )
    await db_session.commit()
