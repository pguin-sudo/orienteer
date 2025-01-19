from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from orienteer.general.data.orienteer.models.choosing_promo import ChoosingPromo
from orienteer.general.data.orienteer.models.ytpromo_code_usages import YTPromotionalCodeUsages

async def check_ytpromo_code_validity(db_session: AsyncSession, code: str) -> ChoosingPromo:
    """
    Проверяет, существует ли промокод с данным кодом, не истёк ли его срок действия,
    и активен ли он.
    """
    query = select(ChoosingPromo).filter_by(code=code, active=True).filter(ChoosingPromo.end_time > datetime.utcnow())

    result = await db_session.execute(query)
    check_promo = result.scalars().first()

    return check_promo

async def mark_ytpromo_as_used(db_session: AsyncSession, user_id: UUID, code: str):
    """
    Добавляет использование промокода пользователем в таблицу 'promotional_code_usages'
    """
    promo_usage = YTPromotionalCodeUsages(user_id=user_id, promotional_code=code)
    db_session.add(promo_usage)
    await db_session.commit()

async def increase_promo_usages(db_session: AsyncSession, code: str):
    """
    Увеличивает счетчик использования промокода на 1 при успешной активации
    """
    await db_session.execute(
        update(ChoosingPromo)
        .where(ChoosingPromo.code == code)
        .values(usages=ChoosingPromo.usages + 1)  # Увеличиваем usages на 1
    )
    await db_session.commit()

async def check_ytpromo_already_used(
    db_session: AsyncSession, user_id: UUID, code: str) -> bool:
    result = await db_session.execute(
        select(YTPromotionalCodeUsages).filter_by(user_id=user_id, promotional_code=code)
    )
    return bool(result.scalars().first())
