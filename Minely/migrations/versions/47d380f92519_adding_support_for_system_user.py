"""Adding support for system user

Revision ID: 47d380f92519
Revises: 
Create Date: 2020-04-09 20:36:41.731747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d380f92519'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('worker', sa.Column('previous_user_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('worker', 'previous_user_id')
    # ### end Alembic commands ###
