from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from orienteer.general.data.orienteer.models.transactions import (
    Transaction,
    TransactionType,
)


async def get_balance(db_session: AsyncSession, user_id: UUID) -> Optional[float]:
    result = await db_session.execute(
        select(func.sum(Transaction.amount)).filter(
            user_id == Transaction.user_id, Transaction.is_active
        )
    )
    balance = result.scalar() or 0.0

    return balance


async def add_transaction(
    db_session: AsyncSession,
    user_id: UUID,
    amount: int,
    t_type: TransactionType = TransactionType.Other,
    name: str | None = None,
) -> None:
    if name is None:
        name = t_type.name
    transaction = Transaction(
        user_id=user_id, name=name, transaction_type=t_type, amount=float(amount)
    )
    db_session.add(transaction)
    await db_session.commit()
