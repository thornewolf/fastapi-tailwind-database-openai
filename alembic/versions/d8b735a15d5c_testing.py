"""testing

Revision ID: d8b735a15d5c
Revises: 333cb90e9f63
Create Date: 2023-09-06 20:54:20.429383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d8b735a15d5c"
down_revision = "333cb90e9f63"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow_stage_elements", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.String(), nullable=True))
        batch_op.create_foreign_key("users", "users", ["user_id"], ["id"])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow_stage_elements", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###
