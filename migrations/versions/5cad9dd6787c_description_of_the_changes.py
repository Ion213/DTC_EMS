"""Description of the changes

Revision ID: 5cad9dd6787c
Revises: 600ddf050934
Create Date: 2025-02-26 09:59:24.254235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cad9dd6787c'
down_revision = '600ddf050934'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.alter_column('student_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('event_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.alter_column('payment_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('transaction_code',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.create_unique_constraint(None, ['transaction_code'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('transaction_code',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=500),
               nullable=True)
        batch_op.alter_column('payment_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.alter_column('event_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('student_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
