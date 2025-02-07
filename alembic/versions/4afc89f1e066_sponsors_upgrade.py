"""sponsors_upgrade

Revision ID: 4afc89f1e066
Revises: 707fa40b4586
Create Date: 2024-08-02 14:00:43.339577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4afc89f1e066'
down_revision: Union[str, None] = '707fa40b4586'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('discord_auth', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('promotional_codes', 'expiration_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('seasons', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.add_column('sponsors', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.alter_column('sponsors', 'extra_slots',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sponsors', 'ooc_color',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('sponsors', 'allowed_markings',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.alter_column('sponsors', 'ghost_theme',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sponsors', 'ghost_theme',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('sponsors', 'allowed_markings',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    op.alter_column('sponsors', 'ooc_color',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('sponsors', 'extra_slots',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('sponsors', 'created_at')
    op.alter_column('seasons', 'start_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('promotional_codes', 'expiration_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('discord_auth', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###
