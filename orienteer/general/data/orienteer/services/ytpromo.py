from datetime import datetime, timedelta, timezone
from uuid import UUID
from ..repositories import ytpromo
from orienteer.bot.utils.content_locale import Errors, Results
from ..database import database_helper
from orienteer.general.data.ss14.repositories import playtime
from orienteer.general.formatting.playtime import get_job_group_and_name
from orienteer.general.formatting.time import get_formatted_timedelta


async def validate_ytpromo_code(db_session, code: str):
    promo = await ytpromo.check_ytpromo_code_validity(db_session, code)
    return promo

async def try_ytpromo(user_id: UUID, code: str, selected_department: str) -> tuple[bool, str, str]:
    code = code.lower()

    async with database_helper.session_factory() as db_session:
        data = await ytpromo.check_ytpromo_code_validity(db_session, code)
        if not data:
            return False, Errors.promo_not_found.value

        if data.end_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return False, Errors.promo_overdue.value

        if await ytpromo.check_ytpromo_already_used_ss14(db_session, user_id, code):
            return False, Errors.promo_used_ss14_account.value

        roles_text_all = {
            "Служба безопасности": {
                "Overall": 600,
                "JobSecurityCadet": 600,
            },
            "Отдел карго": {
                "Overall": 300,
                "JobCargoTechnician": 300,
                "JobSalvageSpecialist": 300,
            },
            "Инженерный отдел": {
                "Overall": 300,
                "JobTechnicalAssistant": 600,
            },
            "Медицинский отдел": {
                "Overall": 300,
                "JobMedicalIntern": 300,
                "JobMedicalDoctor": 300,
            },
            "Научный отдел": {
                "Overall": 300,
                "JobResearchAssistant": 300,
                "JobScientist": 300,
            },
            "Синтетики": {
                "Overall": 300,
                "JobBorg": 600,
            },
            "Сервисный отдел": {
                "Overall": 600,
                "JobServiceWorker": 600,
            },
        }

        roles_for_department = roles_text_all[selected_department]

        roles_text = ""

        for tracker, minutes in roles_for_department.items():
            await playtime.add_playtime(user_id, tracker, minutes)
            roles_text += (f"- **{get_job_group_and_name(tracker)[1]}**: "
                           f"{get_formatted_timedelta(timedelta(minutes=minutes))}\n")

        await ytpromo.mark_ytpromo_as_used(db_session, user_id, code)
        await ytpromo.increase_promo_usages(db_session, code)

        return True, f"Приятной игры на нашем сервере!"
