from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orienteer.general.data.orienteer.models.role_time_coefficients import (
    RoleTimeCoefficient,
)


async def get_coefficients_by_roles(
    db_session: AsyncSession, role_ids: Iterable[int]
) -> int:
    result = await db_session.execute(
        select(RoleTimeCoefficient.coefficient).filter(
            RoleTimeCoefficient.role_id.in_(role_ids)
        )
    )
    return sum(row[0] for row in result.fetchall())
