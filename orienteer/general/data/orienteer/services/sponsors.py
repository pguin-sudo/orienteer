from dataclasses import dataclass
from uuid import UUID

from orienteer.general.config import ROLES_SPONSOR
from orienteer.general.data.orienteer.models.sponsors import Sponsor
from orienteer.general.utils import discord
from ..database import async_session
from ..repositories import sponsors, discord_auth


@dataclass
class SponsorDefaults:
    tier: int = 0
    extra_slots: int = 0
    ooc_color: str = '87cefa'
    allowed_markings: tuple[str] = ('',)
    ghost_theme: str = ''
    have_sponsor_chat: bool = False
    have_priority_join: bool = False


def _have_privileges(sponsor: Sponsor) -> bool:
    if (sponsor.extra_slots == 0 and not sponsor.ooc_color and not sponsor.allowed_markings and not sponsor.ghost_theme
            and not sponsor.have_sponsor_chat and not sponsor.have_priority_join):
        return False
    else:
        return True


async def is_sponsor_active(user_id: UUID) -> bool:
    async with async_session() as db_session:
        sponsor = await sponsors.get_sponsor(db_session, user_id)

    if sponsor is None or not _have_privileges(sponsor) or not sponsor.is_active:
        return False

    return True


async def get_sponsor_status_and_color(user_id: UUID) -> tuple[str | None, int | None]:
    async with async_session() as db_session:
        sponsor = await sponsors.get_sponsor(db_session, user_id)

    if sponsor is None:
        return None, None

    if not _have_privileges(sponsor):
        status = 'Нет активных привилегий'
    elif not sponsor.is_active:
        status = 'Временно отключен'
    else:
        status = 'Активен'

    color = int(sponsor.ooc_color, 16) if sponsor.ooc_color is not None else None

    return status, color


async def get_sponsor_state(user_id: UUID) -> dict:
    async with async_session() as db_session:
        sponsor: Sponsor | None = await sponsors.get_sponsor(db_session, user_id)

        if sponsor is None:
            sponsor_data = {"tier": 1, "extraSlots": SponsorDefaults.extra_slots, "oocColor": SponsorDefaults.ooc_color,
                            "allowedMarkings": SponsorDefaults.allowed_markings,
                            "ghostTheme": SponsorDefaults.ghost_theme,
                            "havePriorityJoin": SponsorDefaults.have_priority_join, }
        else:
            sponsor_data = {"tier": 1,
                            "extraSlots": sponsor.extra_slots if sponsor.extra_slots != 0 else SponsorDefaults.extra_slots,
                            "oocColor": sponsor.ooc_color if sponsor.ooc_color is not None else SponsorDefaults.ooc_color,
                            "allowedMarkings": sponsor.allowed_markings if sponsor.allowed_markings != [] else SponsorDefaults.allowed_markings,
                            "ghostTheme": sponsor.ghost_theme if sponsor.ghost_theme is not None else SponsorDefaults.ghost_theme,
                            "havePriorityJoin": sponsor.have_priority_join if sponsor.have_priority_join is not None else SponsorDefaults.have_priority_join, }

        return {user_id: sponsor_data}


async def get_sponsor(user_id: UUID) -> Sponsor | None:
    async with async_session() as db_session:
        return await sponsors.get_sponsor(db_session, user_id)


async def add_extra_clots(user_id: UUID, amount: int) -> Sponsor | None:
    async with async_session() as db_session:
        sponsor = await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, extra_slots=sponsor.extra_slots + amount)


async def set_colored_nick(user_id: UUID, color: str | None):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, ooc_color=color)


async def set_sponsor_chat(user_id: UUID, status: bool):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        discord_user_id = await discord_auth.get_discord_user_id_by_user_id(db_session, user_id)
        if discord_user_id is None:
            raise Exception
        await discord.set_role(discord_user_id, ROLES_SPONSOR, not status)
        return await sponsors.update_sponsor(db_session, user_id, have_sponsor_chat=status)


async def set_priority_join(user_id: UUID, status: bool):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, have_priority_join=status)


async def add_marking(user_id: UUID, marking: str):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.add_marking(db_session, user_id, marking)


async def remove_marking(user_id: UUID, marking: str):
    async with async_session() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.remove_marking(db_session, user_id, marking)
