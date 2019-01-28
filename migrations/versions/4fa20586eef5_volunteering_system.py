"""volunteering_system

Revision ID: 4fa20586eef5
Revises: ed1b4642f0b1
Create Date: 2019-01-28 06:56:38.362159

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4fa20586eef5'
down_revision = 'ed1b4642f0b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shift_info',
    sa.Column('shift_info_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('coordinator', sa.String(length=32), nullable=True),
    sa.Column('location', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('shift_info_id')
    )
    op.create_table('shift',
    sa.Column('shift_id', sa.Integer(), nullable=False),
    sa.Column('info_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('stop_time', sa.DateTime(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['info_id'], ['shift_info.shift_info_id'], ),
    sa.PrimaryKeyConstraint('shift_id')
    )
    op.create_table('shift_slots',
    sa.Column('slot_id', sa.Integer(), nullable=False),
    sa.Column('shift_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('mandatory', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['shift_id'], ['shift.shift_id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.team_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('slot_id')
    )
    op.drop_table('salsa_partners')
    op.drop_table('polka_partners')
    op.add_column('tournament_state', sa.Column('volunteering_system_open', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournament_state', 'volunteering_system_open')
    op.create_table('polka_partners',
    sa.Column('couple_id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('lead_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('follow_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('couple_id'),
    mysql_collate='utf8_bin',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('salsa_partners',
    sa.Column('couple_id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('lead_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('follow_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('couple_id'),
    mysql_collate='utf8_bin',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('shift_slots')
    op.drop_table('shift')
    op.drop_table('shift_info')
    # ### end Alembic commands ###
