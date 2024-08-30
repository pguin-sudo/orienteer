"""purchases: nullable price

Revision ID: 72c4d236c9f2
Revises: 3578151648d2
Create Date: 2024-08-29 01:44:15.196965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72c4d236c9f2'
down_revision: Union[str, None] = '3578151648d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
