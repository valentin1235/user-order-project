"""version_2

Revision ID: 3b7c3bed41ac
Revises: 87d87ccf97f2
Create Date: 2020-04-27 20:27:44.088671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7c3bed41ac'
down_revision = '87d87ccf97f2'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'pass', new_column_name='password')



def downgrade():
    pass
