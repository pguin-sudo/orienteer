from datetime import timedelta, timezone, datetime

import loguru
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from orienteer.general.config import ROLES_ELDERLING
from orienteer.general.data.orienteer.services import discord_auth
from orienteer.general.data.ss14.services import playtime, seen_time, bans, player
from orienteer.general.utils.discord import set_role


async def check_elderings():
    for auth_data in await discord_auth.get_all_authorized():
        play_time = await playtime.get_overall(auth_data.user_id)
        if (play_time > timedelta(days=14) and datetime.now(timezone.utc) - await seen_time.get_first_seen_time(
            auth_data.user_id) > timedelta(days=31) and (await bans.get_fine(auth_data.user_id)) < 300):
            await set_role(auth_data.discord_user_id, ROLES_ELDERLING, remove=False)
        else:
            await set_role(auth_data.discord_user_id, ROLES_ELDERLING, remove=True)


async def setup_roles_schedule(scheduler: AsyncIOScheduler):
    await check_elderings()
    scheduler.add_job(check_elderings, CronTrigger(hour='*'))
