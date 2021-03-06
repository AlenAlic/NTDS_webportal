"""etds_brno_additions

Revision ID: d5592bf71272
Revises: 3c9e80ff9c9b
Create Date: 2018-06-09 02:43:35.728134 - 2018-09-29 14:54:52.542147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5592bf71272'
down_revision = '3c9e80ff9c9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('additional_info', sa.Column('bus_to_brno', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('polka_partners',
                    sa.Column('couple_id', sa.Integer(), nullable=False),
                    sa.Column('lead_id', sa.Integer(), nullable=False),
                    sa.Column('follow_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('couple_id')
                    )
    op.create_table('salsa_partners',
                    sa.Column('couple_id', sa.Integer(), nullable=False),
                    sa.Column('lead_id', sa.Integer(), nullable=False),
                    sa.Column('follow_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('couple_id')
                    )
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('volunteer_info',
                  sa.Column('level_ballroom', sa.String(length=16), server_default='Below D', nullable=False))
    op.add_column('volunteer_info',
                  sa.Column('level_latin', sa.String(length=16), server_default='Below D', nullable=False))
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('status_info', sa.Column('checked_in', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('status_info', 'checked_in')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('volunteer_info', 'level_latin')
    op.drop_column('volunteer_info', 'level_ballroom')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('salsa_partners')
    op.drop_table('polka_partners')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('additional_info', 'bus_to_brno')
    # ### end Alembic commands ###

