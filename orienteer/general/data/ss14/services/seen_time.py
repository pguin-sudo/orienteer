from uuid import UUID
from datetime import datetime

from orienteer.general.formatting.time import *
from ..repositories import seen_time


async def get_last_seen_time(user_id: UUID) -> datetime | None:
    return get_formatted_datetime(await seen_time.get_last_seen_time(user_id))


async def get_first_seen_time(user_id: UUID) -> datetime | None:
    return get_formatted_datetime(await seen_time.get_first_seen_time(user_id))
