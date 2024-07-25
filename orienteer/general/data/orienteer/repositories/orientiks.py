from loguru import logger
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.orientiks import Orientiks


async def get_balance_raw_info(db_session: AsyncSession, user_id: str) -> dict | None:
    result = await db_session.execute(select(Orientiks).where(Orientiks.user_id == user_id))
    row = result.fetchone()
    if row is not None:
        return row[0]
    else:
        return None


async def add_time_balancing(db_session: AsyncSession, user_id: str, time_balancing: int) -> None:
    result = await db_session.execute(select(Orientiks).where(Orientiks.user_id == user_id))
    record = result.scalars().first()

    if record:
        new_time_balancing = record.time_balancing + time_balancing
        await db_session.execute(
            update(Orientiks)
            .where(Orientiks.user_id == user_id)
            .values(time_balancing=new_time_balancing)
        )
    else:
        await db_session.execute(
            insert(Orientiks).values(user_id=user_id,
                                     time_balancing=time_balancing)
        )

    await db_session.commit()


async def add_orientiks_from_friends(db_session: AsyncSession, user_id: str, amount: int) -> None:
    result = await db_session.execute(select(Orientiks).where(Orientiks.user_id == user_id))
    record = result.scalars().first()

    if record:
        new_friends_amount = record.friends + amount
        await db_session.execute(
            update(Orientiks)
            .where(Orientiks.user_id == user_id)
            .values(friends=new_friends_amount)
        )
    else:
        await db_session.execute(
            insert(Orientiks).values(user_id=user_id, friends=amount)
        )

    await db_session.commit()


async def add_spent(db_session: AsyncSession, user_id: str, amount: int) -> None:
    current_spent = await db_session.scalar(select(Orientiks.spent).where(Orientiks.user_id == user_id))
    new_spent = current_spent + amount
    await db_session.execute(update(Orientiks).where(Orientiks.user_id == user_id).values(spent=new_spent))
    await db_session.commit()
