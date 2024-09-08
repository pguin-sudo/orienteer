from typing import Any
from uuid import UUID

from ..repositories import admin_rank, playtime


# TODO: REPOSITORY SESSION
async def get_admin_rank_name_and_time(user_id: UUID) -> tuple[str | None, Any] | None:
    rank_id = await admin_rank.get_admin_rank_id(user_id)
    rank_time = await playtime.get_tracker(user_id, "Admin")
    if rank_id is not None and rank_time is not None:
        return await admin_rank.get_rank_name(rank_id), rank_time["time_spent"]
    else:
        return None
