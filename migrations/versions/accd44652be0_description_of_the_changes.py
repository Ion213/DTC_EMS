"""Description of the changes

Revision ID: accd44652be0
Revises: 8bab107cc39b
Create Date: 2025-02-21 19:10:48.875252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'accd44652be0'
down_revision = '8bab107cc39b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.alter_column('attendance_status',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Enum('present', 'missed_out', name='attendance_status'),
               existing_nullable=True)
        batch_op.drop_column('payment_status')

    with op.batch_alter_table('schedule', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_status', sa.Enum('Paid', 'Unpaid', name='payment_status'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedule', schema=None) as batch_op:
        batch_op.drop_column('payment_status')

    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_status', sa.VARCHAR(length=50), nullable=True))
        batch_op.alter_column('attendance_status',
               existing_type=sa.Enum('present', 'missed_out', name='attendance_status'),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###
