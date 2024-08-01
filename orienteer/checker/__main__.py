import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from loguru_discord import DiscordSink

from orienteer.checker.schedules.bans import setup_bans_schedule
from orienteer.checker.schedules.seasons import setup_seasons_schedule, check_season_and_update
from orienteer.general.config.local import WEBHOOKS_LOGS

logger.add(DiscordSink(WEBHOOKS_LOGS['checker']))


async def main():
    scheduler = AsyncIOScheduler()

    await check_season_and_update()
    setup_bans_schedule(scheduler)
    setup_seasons_schedule(scheduler)

    scheduler.start()

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
