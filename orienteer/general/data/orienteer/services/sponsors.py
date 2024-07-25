import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import UUID

from orienteer.general.data.orienteer.models.sponsors import Sponsor

from ..repositories import sponsors
from ..database import async_session

from orienteer.general.formatting.time import get_formatted_datetime


async def get_sponsor_status_and_color(user_id: UUID) -> tuple[str | None, int | None]:
    async with async_session() as db_session:
        sponsor = await sponsors.get_sponsor(db_session, user_id)

    if sponsor is None:
        return None, None

    status = 'Активен' if sponsor.is_active else 'Временно отключен'

    return status, int(sponsor.ooc_color, 16)


async def get_sponsor_as_dict(user_id: UUID) -> dict:
    async with async_session() as db_session:
        sponsor: Sponsor = await sponsors.get_sponsor(db_session, user_id)
        return {
            user_id: {
                "tier": 1,
                "extraSlots": sponsor.extra_slots,
                "oocColor": sponsor.ooc_color,
                "allowedMarkings": sponsor.allowed_markings,
                "ghostTheme": sponsor.ghost_theme,
                "havePriorityJoin": sponsor.have_priority_join,
            }}


async def set_colored_nick(user_id: UUID, color):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, ooc_color=color)


async def set_sponsor_chat(user_id: UUID, status):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, have_sponsor_chat=status)


async def set_priority_queue(user_id: UUID, status):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, have_queue_priority=status)


async def add_marking(user_id: UUID, marking: str):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.add_marking(db_session, user_id, marking)


async def remove_marking(user_id: UUID, marking: str):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.remove_marking(db_session, user_id, marking)


async def set_activation(user_id: UUID, status):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, is_active=status)
