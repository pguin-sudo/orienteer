import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from loguru_discord import DiscordSink

from orienteer.checker.schedules.bans import setup_bans_schedule
from orienteer.general.config.local import WEBHOOKS_LOGS

logger.add(DiscordSink(WEBHOOKS_LOGS['checker']))


async def main():
    scheduler = AsyncIOScheduler()

    setup_bans_schedule(scheduler)

    scheduler.start()

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
