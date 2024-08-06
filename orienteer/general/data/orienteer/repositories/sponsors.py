from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from orienteer.general.data.orienteer.models.sponsors import Sponsor


async def get_sponsor(db_session: AsyncSession, user_id) -> Sponsor | None:
    sponsor = (await db_session.execute(select(Sponsor).filter_by(user_id=user_id))).fetchone()
    sponsor = sponsor[0] if sponsor is not None else None
    return sponsor


async def try_create_empty_sponsor(db_session: AsyncSession, user_id) -> Sponsor:
    sponsor = (await db_session.execute(select(Sponsor).filter_by(user_id=user_id))).fetchone()
    if sponsor is None:
        sponsor = Sponsor(user_id)
        db_session.add(sponsor)
        await db_session.commit()
        await db_session.refresh(sponsor)
        return sponsor
    return sponsor[0]


async def update_sponsor(db_session: AsyncSession, user_id, **kwargs) -> Sponsor | None:
    sponsor = (await db_session.execute(select(Sponsor).filter_by(user_id=user_id))).fetchone()
    if sponsor is not None:
        sponsor = sponsor[0]
        for key, value in kwargs.items():
            setattr(sponsor, key, value)
        await db_session.commit()
        return sponsor
    return None


async def add_marking(db_session: AsyncSession, user_id, marking):
    sponsor = (await db_session.execute(select(Sponsor).filter_by(user_id=user_id))).fetchone()
    if sponsor is not None:
        sponsor = sponsor[0]
        sponsor.allowed_markings.append(marking)
        await db_session.commit()
        return sponsor
    return None


async def remove_marking(db_session: AsyncSession, user_id, marking):
    sponsor = (await db_session.execute(select(Sponsor).filter_by(user_id=user_id))).fetchone()
    if sponsor is not None:
        if marking in sponsor.allowed_markings:
            sponsor.allowed_markings.remove(marking)
            await db_session.commit()
        return sponsor
    return None
