"""purchases: true nullable price

Revision ID: 37c7160a6a3a
Revises: 72c4d236c9f2
Create Date: 2024-08-30 11:15:49.002545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37c7160a6a3a'
down_revision: Union[str, None] = '72c4d236c9f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
