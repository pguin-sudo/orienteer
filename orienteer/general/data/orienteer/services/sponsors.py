from uuid import UUID

from orienteer.general.config import ROLES_GIGACHAT
from orienteer.general.utils import discord
from ..database import database_helper
from ..models.sponsors import Sponsor
from ..repositories import sponsors, discord_auth


def _have_privileges(sponsor: Sponsor) -> bool:
    if (
            sponsor.extra_slots == 0 and not sponsor.ooc_color and not sponsor.allowed_markings and not sponsor.ghost_theme and not sponsor.sponsor_chat and not sponsor.priority_join):
        return False
    else:
        return True


async def is_sponsor_active(user_id: UUID) -> bool:
    async with database_helper.session_factory() as db_session:
        sponsor = await sponsors.get_sponsor(db_session, user_id)

    if sponsor is None or not _have_privileges(sponsor) or not sponsor.is_active:
        return False

    return True


async def get_sponsor_status_and_color(user_id: UUID) -> tuple[str | None, int | None]:
    async with database_helper.session_factory() as db_session:
        sponsor = await sponsors.get_sponsor(db_session, user_id)

    if sponsor is None:
        return None, None

    if not _have_privileges(sponsor):
        status = 'Нет активных привилегий 🩼'
    elif not sponsor.is_active:
        status = 'Временно отключен 🛞'
    else:
        status = 'Активен 🎗️'

    color = int(sponsor.ooc_color, 16) if sponsor.ooc_color is not None else None

    return status, color


async def get_sponsor_state(user_id: UUID) -> dict | None:
    async with database_helper.session_factory() as db_session:
        sponsor: Sponsor | None = await sponsors.get_sponsor(db_session, user_id)

        if sponsor is None:
            return None

        sponsor_data = {
            'tier': 1,
            'priorityJoin': sponsor.priority_join,
            'extraSlots': sponsor.extra_slots,
            'allowedMarkings': sponsor.allowed_markings,
            'loadouts': sponsor.loadouts,
            'openAllRoles': sponsor.open_all_roles,
            'ghostTheme': sponsor.ghost_theme}

        if sponsor.ooc_color is not None:
            sponsor_data['oocColor'] = f'#{sponsor.ooc_color}'

        if sponsor.ghost_theme is not None:
            sponsor_data['ghost_theme'] = f'{sponsor.ghost_theme}'

        return sponsor_data


async def get_sponsor(user_id: UUID) -> Sponsor | None:
    async with database_helper.session_factory() as db_session:
        return await sponsors.get_sponsor(db_session, user_id)


async def add_extra_clots(user_id: UUID, amount: int) -> Sponsor | None:
    async with database_helper.session_factory() as db_session:
        sponsor = await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, extra_slots=sponsor.extra_slots + amount)


async def set_colored_nick(user_id: UUID, color: str | None):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, ooc_color=color)


async def set_sponsor_chat(user_id: UUID, status: bool):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        discord_user_id = await discord_auth.get_discord_user_id_by_user_id(db_session, user_id)
        if discord_user_id is None:
            raise Exception
        await discord.set_role(discord_user_id, ROLES_GIGACHAT, not status)
        return await sponsors.update_sponsor(db_session, user_id, sponsor_chat=status)


async def set_priority_join(user_id: UUID, status: bool):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.update_sponsor(db_session, user_id, priority_join=status)


async def add_marking(user_id: UUID, marking: str):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.add_marking(db_session, user_id, marking)


async def remove_marking(user_id: UUID, marking: str):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.remove_marking(db_session, user_id, marking)


async def add_laodout(user_id: UUID, marking: str):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.add_loadout(db_session, user_id, marking)


async def remove_laodout(user_id: UUID, marking: str):
    async with database_helper.session_factory() as db_session:
        await sponsors.try_create_empty_sponsor(db_session, user_id)
        return await sponsors.remove_loadout(db_session, user_id, marking)
