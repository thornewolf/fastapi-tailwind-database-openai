"""default message

Revision ID: 7b2ee66113f9
Revises: 223e213d576f
Create Date: 2023-11-10 12:46:51.545842

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '7b2ee66113f9'
down_revision = '223e213d576f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('function_executions')
    op.drop_table('functions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('functions',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('template', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('preprocess_function', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.VARCHAR(), nullable=True),
    sa.Column('execution_count', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('function_executions',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('function_id', sa.VARCHAR(), nullable=True),
    sa.Column('start_time', sa.FLOAT(), nullable=True),
    sa.Column('completion_time', sa.FLOAT(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('input', sqlite.JSON(), nullable=True),
    sa.Column('output', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['function_id'], ['functions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
