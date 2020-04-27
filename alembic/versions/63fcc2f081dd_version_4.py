"""version_4

Revision ID: 63fcc2f081dd
Revises: 81b410a8b8e3
Create Date: 2020-04-28 00:03:14.965170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63fcc2f081dd'
down_revision = '81b410a8b8e3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), default=False))
    op.add_column('boards', sa.Column('is_deleted', sa.Boolean(), default=False))
    op.add_column('articles', sa.Column('is_deleted', sa.Boolean(), default=False))


def downgrade():
    pass
