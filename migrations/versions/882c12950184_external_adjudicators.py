"""external_adjudicators

Revision ID: 882c12950184
Revises: 0aae269b5125
Create Date: 2019-10-03 22:19:14.418149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882c12950184'
down_revision = '0aae269b5125'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournament_state', sa.Column('external_adjudicator_registration_open', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournament_state', 'external_adjudicator_registration_open')
    # ### end Alembic commands ###
