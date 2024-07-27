import asyncio
from datetime import datetime, timezone

from loguru import logger


async def check_roles():
    logger.debug('Роли проверяются...')


async def schedule_roles():
    await asyncio.sleep((datetime.now(timezone.utc).minute % 5)*60)
    while True:
        await check_roles()
        await asyncio.sleep(60*5)
