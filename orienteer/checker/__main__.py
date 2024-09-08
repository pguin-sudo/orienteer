import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from loguru_discord import DiscordSink

from orienteer.checker.schedules.bans import setup_bans_schedule
from orienteer.checker.schedules.orientiks import setup_orientiks_schedule
from orienteer.checker.schedules.roles import setup_roles_schedule
from orienteer.checker.schedules.seasons import setup_seasons_schedule
from orienteer.checker.schedules.subscriptions import setup_subscriptions_schedule
from orienteer.general.config import WEBHOOKS_LOGS

logger.add(DiscordSink(WEBHOOKS_LOGS["checker"]))


async def main():
    logger.success("<<<<<<<<<<<<<<<< Checker module is starting >>>>>>>>>>>>>>>>")

    scheduler = AsyncIOScheduler()

    await setup_bans_schedule(scheduler)
    await setup_orientiks_schedule(scheduler)
    await setup_roles_schedule(scheduler)
    await setup_seasons_schedule(scheduler)
    await setup_subscriptions_schedule(scheduler)

    scheduler.start()

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
