import asyncio
from datetime import timedelta

from uuid import UUID

from core.data.discord_time import timedelta_to_russian_text
from core.data import ss14

import logging

from core.data.ss14 import get_all_user_ids

logger = logging.getLogger('playtime_clamp')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('playtime_clamp.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(NAME)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


async def playtime_clamp_by_user_id(user_id: UUID):
    overall = await ss14.get_playtime_timedelta(user_id, 'Overall')
    if overall is None:
        return

    time = await ss14.get_all_playtime(user_id)
    if overall is None:
        return

    time = sum([record['time_spent'].total_seconds() for record in time if record['tracker'] != 'Overall'])

    logger.info(f"Playtime for {user_id}: {await timedelta_to_russian_text(timedelta=timedelta(seconds=time))}")

    puk = time - overall.total_seconds()
    if puk < 0:
        logger.error(
            f'Mudila detekted: {user_id} (Difference: {await timedelta_to_russian_text(timedelta=timedelta(seconds=puk))})')
        await ss14.add_playtime(user_id, 'Overall', int(puk / 60))
        return True
    else:
        return False


async def process_all_users():
    async for user_id in get_all_user_ids():
        await playtime_clamp_by_user_id(user_id)


if __name__ == "__main__":
    asyncio.run(process_all_users())
