"""Description of the changes

Revision ID: 07f17fe20359
Revises: f06fbb7d7168
Create Date: 2025-02-11 13:55:39.261472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07f17fe20359'
down_revision = 'f06fbb7d7168'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_out', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_column('time_out')

    # ### end Alembic commands ###
