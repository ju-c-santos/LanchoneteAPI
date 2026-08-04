"""adicionando um novo perfil

Revision ID: 2618e206df6f
Revises: 4cb60dee7ec1
Create Date: 2026-08-04 08:27:29.673708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2618e206df6f'
down_revision = '4cb60dee7ec1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TYPE perfil "
        "ADD VALUE IF NOT EXISTS 'GESTAO'"
    )


def downgrade():
    pass
