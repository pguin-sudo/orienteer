from uuid import UUID

from core.data import ss14
from core.data.orientiks import get_balance

REASON = 'Превышение порога штрафов'


async def ban_if_fine_limit(user_id: UUID, reason: str):
    if await get_balance(user_id) < -500 and reason != REASON:
        await ss14.add_ban(user_id, REASON)
