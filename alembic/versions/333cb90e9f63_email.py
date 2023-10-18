"""email

Revision ID: 333cb90e9f63
Revises: 3613a45aa3bc
Create Date: 2023-08-27 14:40:59.617023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '333cb90e9f63'
down_revision = '3613a45aa3bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('email')

    # ### end Alembic commands ###