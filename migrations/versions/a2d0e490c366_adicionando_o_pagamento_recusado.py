"""adicionando o pagamento recusado

Revision ID: a2d0e490c366
Revises: ae7c6764d4a7
Create Date: 2026-08-01 20:49:02.048943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2d0e490c366'
down_revision = 'ae7c6764d4a7'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        ALTER TYPE status
        ADD VALUE IF NOT EXISTS 'PAGAMENTO_RECUSADO';
    """)


def downgrade():
    pass
