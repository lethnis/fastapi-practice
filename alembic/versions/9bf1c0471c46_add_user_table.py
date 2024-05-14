"""add user table

Revision ID: 9bf1c0471c46
Revises: 2c617f435fa3
Create Date: 2024-05-14 15:13:41.621556

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9bf1c0471c46"
down_revision: Union[str, None] = "2c617f435fa3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
