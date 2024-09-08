from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytz

from orienteer.bot.utils.content_locale import Errors, Results
from orienteer.general.data.ss14.repositories import playtime
from orienteer.general.formatting.playtime import get_job_group_and_name
from orienteer.general.formatting.time import get_formatted_timedelta
from ..database import database_helper
from ..repositories import promo


async def get_creator_code(user_id) -> str | None:
    async with database_helper.session_factory() as db_session:
        return await promo.get_creator_code(db_session, user_id)


async def try_promo(discord_user_id: int, user_id: UUID, code: str) -> tuple[bool, str]:
    # TODO: Lower only to official promos
    code = code.lower()

    async with database_helper.session_factory() as db_session:
        data = await promo.get_promo_data(db_session, code)
        if not data or not data.usages:
            return False, Errors.promo_not_found.value

        if data.usages <= 0:
            return False, Errors.promo_used_max_times.value

        for tracker, time_needed in data.dependencies.items():
            time = await playtime.get_playtime_timedelta(user_id, tracker)
            if not time:
                return False, Errors.no_playtime_info.value
            elif time.total_seconds() / 60 < time_needed:
                return False, Errors.not_enough_playtime.value

        if pytz.UTC.localize(data.expiration_date) < datetime.now(timezone.utc):
            return False, Errors.promo_overdue.value

        if await promo.check_promo_already_used_discord(
            db_session, discord_user_id, code
        ):
            return False, Errors.promo_used_discord_account.value

        if await promo.check_promo_already_used_ss14(db_session, user_id, code):
            return False, Errors.promo_used_ss14_account.value

        creator_code = await promo.get_creator_code(db_session, user_id)

        is_creators_code = data.is_creator
        if is_creators_code and creator_code is not None:
            return False, f"{Errors.creator_promo_used.value} ({creator_code})"

        roles_text = ""

        for tracker, minutes in data.jobs.items():
            await playtime.add_playtime(user_id, tracker, minutes)
            roles_text = f"**{get_job_group_and_name(tracker)[1]}**: {get_formatted_timedelta(timedelta(minutes=minutes))}"

        await promo.mark_promo_as_used(db_session, user_id, discord_user_id, code)
        await promo.decrease_promo_usages(db_session, code)

        return (
            True,
            (
                f"{Results.you_have_received.value} {roles_text}\n"
                f'{Results.now_you_have_support_creator.value} "{code}"'
                if is_creators_code
                else ""
            ),
        )
