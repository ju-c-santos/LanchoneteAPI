"""renomeia canal do pedido

Revision ID: 53fc195a5e1b
Revises: cc4793f5680b
Create Date: 2026-08-06 23:30:00.407341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53fc195a5e1b'
down_revision = 'cc4793f5680b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "pedido",
        "canalpedido",
        new_column_name="local_pedido"
    )


def downgrade():
    op.alter_column(
        "pedido",
        "local_pedido",
        new_column_name="canalpedido"
    )
