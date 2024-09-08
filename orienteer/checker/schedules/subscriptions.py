from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from loguru import logger

from orienteer.general.data.orienteer.services import purchases
from orienteer.general.formatting.time import get_formatted_datetime


async def setup_retrieves_schedule(scheduler: AsyncIOScheduler):
    current_subscriptions = await purchases.get_current_subscriptions()

    for purchase, product in current_subscriptions:
        if scheduler.get_job(f"retrieve_{purchase.user_id}_{product.id}") is not None:
            continue

        retrieve_date = purchase.date + product.cooldown

        logger.debug(
            f"Scheduling retrieval for Purchase ({purchase}) of Product ({product}) at "
            f"{get_formatted_datetime(retrieve_date)}"
        )

        scheduler.add_job(
            product.retrieve,
            DateTrigger(retrieve_date),
            args=[purchase.user_id],
            id=f"retrieve_{purchase.user_id}_{product.id}",
        )


async def setup_subscriptions_schedule(scheduler: AsyncIOScheduler):
    scheduler.add_job(
        setup_retrieves_schedule, CronTrigger(minute="*/2"), args=[scheduler]
    )
