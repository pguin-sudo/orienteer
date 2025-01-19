"""Add ytpromo_code_usages table

Revision ID: ba2ac85301e8
Revises: 297b7481d309
Create Date: 2025-01-18 11:52:37.169984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ba2ac85301e8'
down_revision: Union[str, None] = '297b7481d309'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "ytpromo_code_usages",
        sa.Column("cache_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "promotional_code",
            sa.String,
            sa.ForeignKey("choosing_promo.code"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade():
    op.drop_table("ytpromo_code_usages")
