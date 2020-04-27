"""version_3

Revision ID: 81b410a8b8e3
Revises: 3b7c3bed41ac
Create Date: 2020-04-27 20:34:29.263194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81b410a8b8e3'
down_revision = '3b7c3bed41ac'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('boards', 'user_id', new_column_name='uploader')
    op.alter_column('articles', 'user_id', new_column_name='uploader')


def downgrade():
    pass
