from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from orienteer.general.data.orienteer.services import orientiks


async def add_orientiks_cache_info():
    new_info = await orientiks.add_calculated_cached_info()
    logger.debug(f'New info: {new_info}')


async def setup_orientiks_schedule(scheduler: AsyncIOScheduler):
    await add_orientiks_cache_info()

    scheduler.add_job(add_orientiks_cache_info, CronTrigger(minute='*/10'))
