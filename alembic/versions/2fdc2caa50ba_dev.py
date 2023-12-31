"""dev

Revision ID: 2fdc2caa50ba
Revises: 
Create Date: 2023-08-25 12:55:01.217257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2fdc2caa50ba"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("function_executions", schema=None) as batch_op:
        batch_op.add_column(sa.Column("function_id", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("execution_time", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("status", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("input", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("output", sa.String(), nullable=True))
        batch_op.create_foreign_key("functions", "functions", ["function_id"], ["id"])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("function_executions", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("output")
        batch_op.drop_column("input")
        batch_op.drop_column("status")
        batch_op.drop_column("execution_time")
        batch_op.drop_column("function_id")

    # ### end Alembic commands ###
