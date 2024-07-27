from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orienteer.general.data.orienteer.models.promotional_code import PromotionalCode
from orienteer.general.data.orienteer.models.promotional_code_usages import PromotionalCodeUsages


async def get_promo_data(db_session: AsyncSession, code: str) -> PromotionalCode:
    result = await db_session.execute(select(PromotionalCode).filter_by(code=code))
    return result.scalars().first()


async def get_creator_code(db_session: AsyncSession, user_id: str) -> str | None:
    creator_codes = await db_session.execute(select(PromotionalCode.code).filter_by(is_creator=True))
    creator_codes = creator_codes.scalars().all()

    for creator_code in creator_codes:
        exists = await db_session.execute(select(PromotionalCodeUsages).filter_by(user_id=user_id, promotional_code=creator_code))
        if exists.scalars().first():
            return creator_code

    return None


async def check_promo_already_used_discord(db_session: AsyncSession, discord_user_id: int, code: str) -> bool:
    result = await db_session.execute(select(PromotionalCodeUsages).filter_by(discord_user_id=discord_user_id, promotional_code=code))
    return bool(result.scalars().first())


async def check_promo_already_used_ss14(db_session: AsyncSession, user_id: str, code: str) -> bool:
    result = await db_session.execute(select(PromotionalCodeUsages).filter_by(user_id=user_id, promotional_code=code))
    return bool(result.scalars().first())


async def mark_promo_as_used(db_session: AsyncSession, user_id: str, discord_user_id: int, code: str):
    db_session.add(PromotionalCodeUsages(user_id=user_id,
                   discord_user_id=discord_user_id, promotional_code=code))
    await db_session.commit()


async def decrease_promo_usages(db_session: AsyncSession, code: str):
    await db_session.execute(update(PromotionalCode).where(PromotionalCode.code == code).values(usages=PromotionalCode.usages - 1))
    await db_session.commit()
