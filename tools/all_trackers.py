import asyncio

from loguru import logger

from orienteer.general.data.ss14.dbconnection import DBConnectionContextManager
from orienteer.general.formatting.playtime import get_job_group_and_name


async def unique_trackers() -> list:
    async with DBConnectionContextManager() as connection:
        return await connection.fetch('SELECT DISTINCT tracker FROM play_time;')


def main():
    tracker_records = asyncio.run(unique_trackers())
    for tracker_record in tracker_records:
        logger.info(get_job_group_and_name(tracker_record['tracker'])[1])


if __name__ == '__main__':
    main()
