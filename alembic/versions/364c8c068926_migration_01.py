"""migration_01

Revision ID: 364c8c068926
Revises: dc06f8767847
Create Date: 2020-04-30 19:02:38.604312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '364c8c068926'
down_revision = 'dc06f8767847'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'random_keys',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('key', sa.String(50), nullable=False),
    )


def downgrade():
    pass
