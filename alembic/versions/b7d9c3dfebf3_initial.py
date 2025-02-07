"""initial

Revision ID: b7d9c3dfebf3
Revises: 
Create Date: 2024-07-25 00:42:49.897234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7d9c3dfebf3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discord_auth',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('discord_user_id', sa.BigInteger(), nullable=False),
    sa.Column('discord_username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('discord_user_id'),
    sa.UniqueConstraint('discord_username')
    )
    op.create_table('orientiks',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('sponsorship', sa.Integer(), nullable=True),
    sa.Column('friends', sa.Integer(), nullable=True),
    sa.Column('pardons', sa.Integer(), nullable=True),
    sa.Column('time_balancing', sa.Integer(), nullable=True),
    sa.Column('spent', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('promotional_codes',
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('usages', sa.Integer(), nullable=False),
    sa.Column('jobs', sa.JSON(), nullable=False),
    sa.Column('dependencies', sa.JSON(), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=True),
    sa.Column('is_creator', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('purchases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sent_bans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_sent_ban_id', sa.Integer(), nullable=True),
    sa.Column('last_sent_role_ban_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sponsors',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('extra_slots', sa.Integer(), nullable=False),
    sa.Column('ooc_color', sa.String(), nullable=False),
    sa.Column('allowed_markings', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('ghost_theme', sa.String(), nullable=False),
    sa.Column('have_sponsor_chat', sa.Boolean(), nullable=False),
    sa.Column('have_priority_join', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('promotional_code_usages',
    sa.Column('cache_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('promotional_code', sa.String(), nullable=False),
    sa.Column('discord_user_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['promotional_code'], ['promotional_codes.code'], ),
    sa.PrimaryKeyConstraint('cache_id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promotional_code_usages')
    op.drop_table('sponsors')
    op.drop_table('sent_bans')
    op.drop_table('purchases')
    op.drop_table('promotional_codes')
    op.drop_table('orientiks')
    op.drop_table('discord_auth')
    # ### end Alembic commands ###
