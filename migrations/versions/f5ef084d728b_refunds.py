"""refunds

Revision ID: f5ef084d728b
Revises: faffbc0bc3ca
Create Date: 2019-06-21 14:43:02.814116

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5ef084d728b'
down_revision = 'faffbc0bc3ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refund',
    sa.Column('refund_id', sa.Integer(), nullable=False),
    sa.Column('payment_info_id', sa.Integer(), nullable=True),
    sa.Column('reason', sa.String(length=128), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('merchandise_purchased_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['merchandise_purchased_id'], ['merchandise_purchase.merchandise_purchased_id'], ),
    sa.ForeignKeyConstraint(['payment_info_id'], ['payment_info.contestant_id'], ),
    sa.PrimaryKeyConstraint('refund_id')
    )
    op.add_column('system_configuration', sa.Column('finances_refund', sa.Boolean(), nullable=False))
    op.add_column('system_configuration', sa.Column('finances_refund_percentage', sa.Integer(), nullable=False))
    op.drop_column('system_configuration', 'finances_partial_refund_percentage')
    op.drop_column('system_configuration', 'finances_full_refund')
    op.drop_column('system_configuration', 'finances_partial_refund')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('system_configuration', sa.Column('finances_partial_refund', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('system_configuration', sa.Column('finances_full_refund', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('system_configuration', sa.Column('finances_partial_refund_percentage', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('system_configuration', 'finances_refund_percentage')
    op.drop_column('system_configuration', 'finances_refund')
    op.drop_table('refund')
    # ### end Alembic commands ###