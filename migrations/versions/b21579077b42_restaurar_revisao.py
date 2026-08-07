"""Restaura a revisão b21579077b42.

Revision ID: b21579077b42
Revises: 53fc195a5e1b
"""

revision = "b21579077b42"
down_revision = "53fc195a5e1b"
branch_labels = None
depends_on = None

from alembic import op

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