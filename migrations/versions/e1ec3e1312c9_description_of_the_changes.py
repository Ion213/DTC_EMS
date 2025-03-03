"""Description of the changes

Revision ID: e1ec3e1312c9
Revises: f3fbbf5dc138
Create Date: 2025-02-19 18:39:28.947353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1ec3e1312c9'
down_revision = 'f3fbbf5dc138'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_column('amount_due')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount_due', sa.FLOAT(), nullable=False))

    # ### end Alembic commands ###
