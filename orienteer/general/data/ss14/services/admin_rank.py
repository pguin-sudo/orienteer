from uuid import UUID
from ..dbhandler import DBHandler

from ..repositories import admin_rank


async def get_admin_rank_name(user_id: UUID) -> int | None:
    rank_id = await admin_rank.get_admin_rank_id(user_id)
    if rank_id is not None:
        return await admin_rank.get_rank_name(rank_id)
    else:
        return None
