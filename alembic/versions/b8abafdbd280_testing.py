"""testing

Revision ID: b8abafdbd280
Revises: 0ec06bbb2b66
Create Date: 2023-09-08 11:38:38.198860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8abafdbd280'
down_revision = '0ec06bbb2b66'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flows')
    op.drop_table('flow_stage_functions')
    op.drop_table('flow_stages')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flow_stages',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=True),
    sa.Column('flow_id', sa.VARCHAR(), nullable=True),
    sa.Column('parent_stage_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['flow_id'], ['flows.id'], ),
    sa.ForeignKeyConstraint(['parent_stage_id'], ['flow_stages.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flow_stage_functions',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=True),
    sa.Column('function_id', sa.VARCHAR(), nullable=True),
    sa.Column('flow_stage_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['flow_stage_id'], ['flow_stages.id'], ),
    sa.ForeignKeyConstraint(['function_id'], ['functions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flows',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###