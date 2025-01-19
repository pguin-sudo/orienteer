"""Add choosing_promo table

Revision ID: 297b7481d309
Revises: 463ed07d6b4a
Create Date: 2025-01-17 15:13:22.280605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '297b7481d309'
down_revision: Union[str, None] = '463ed07d6b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаём таблицу choosing_promo с "code" в качестве первичного ключа
    op.create_table(
        'choosing_promo',
        sa.Column('code', sa.String(length=255), primary_key=True, nullable=False),  # Тут код с PK. Так надо для совместимости с "promotional_code_usages"
        sa.Column('youtuber', sa.String(length=255), nullable=False),                # Имя ютубера
        sa.Column('usages', sa.Integer, nullable=False, server_default='0'),         # ИНОЙ ПОДСЧЁТ! Считает количество активаций от 0. i++ при успешной активации
        sa.Column('end_time', sa.TIMESTAMP, nullable=False),                         # Дата окончания действия
        sa.Column('active', sa.Boolean, nullable=False, server_default='true')       # Статус активности. Можно вырубить на время, не трогая срок
    )


def downgrade() -> None:
    # Удаляем таблицу choosing_promo
    op.drop_table('choosing_promo')
