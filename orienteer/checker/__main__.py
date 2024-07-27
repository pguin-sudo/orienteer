import asyncio
from loguru import logger

from orienteer.checker.bans_checker.__main__ import schedule_bans
from orienteer.checker.roles_checker.__main__ import schedule_roles
from orienteer.checker.seasons_checker.__main__ import schedule_seasons
from orienteer.checker.subscriptions_checker.__main__ import schedule_subscriptions


if __name__ == '__main__':
    logger.info('Running bans checker...')
    asyncio.run(schedule_bans())

    logger.info('Running roles checker...')
    asyncio.run(schedule_roles())

    logger.info('Running roles checker...')
    asyncio.run(schedule_seasons())

    logger.info('Running subscriptions checker...')
    asyncio.run(schedule_subscriptions())
