"""remove_discord_user_id_promo_usages

Revision ID: 463ed07d6b4a
Revises: 84606e16698a
Create Date: 2024-10-03 18:53:29.018779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '463ed07d6b4a'
down_revision: Union[str, None] = '84606e16698a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orientiks_cached_infos')
    op.drop_table('orientiks')
    op.drop_column('promotional_code_usages', 'discord_user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotional_code_usages', sa.Column('discord_user_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.create_table('orientiks',
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('sponsorship', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('friends', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('pardons', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('time_balancing', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('spent', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('user_id', name='orientiks_pkey')
    )
    op.create_table('orientiks_cached_infos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('total_sponsorship', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_friends', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_pardons', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_time_balancing', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_spent', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_fine', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_from_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='orientiks_cached_infos_pkey')
    )
    # ### end Alembic commands ###
