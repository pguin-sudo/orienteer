from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.purchases import Purchase


async def create_purchase(
    db_session: AsyncSession, product_id: int, user_id: UUID, price: int | None
) -> Purchase:
    purchase = Purchase(product_id=product_id, user_id=user_id, price=price)
    db_session.add(purchase)
    await db_session.commit()
    await db_session.refresh(purchase)
    return purchase


async def get_last_purchase_of_product(
    db_session: AsyncSession, user_id: UUID, product_id: int
):
    stmt = (
        select(Purchase)
        .filter(user_id == Purchase.user_id)
        .filter(product_id == Purchase.product_id)
        .order_by(desc(Purchase.date))
        .limit(1)
    )

    result = await db_session.execute(stmt)
    row = result.fetchone()

    if row is not None:
        return row[0]
    else:
        return None


async def get_all_purchases(db_session: AsyncSession) -> tuple[Purchase, ...]:
    result = await db_session.execute(select(Purchase).order_by(desc(Purchase.date)))
    return tuple(result.scalars().all())


async def get_all_purchases_of_user(
    db_session: AsyncSession, user_id: UUID
) -> tuple[Purchase, ...]:
    result = await db_session.execute(
        select(Purchase)
        .filter(user_id == Purchase.user_id)
        .order_by(desc(Purchase.date))
    )
    return tuple(result.scalars().all())
