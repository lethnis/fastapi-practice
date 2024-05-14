"""add content column to posts table

Revision ID: 2c617f435fa3
Revises: 98144d45100c
Create Date: 2024-05-14 15:08:14.306189

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2c617f435fa3"
down_revision: Union[str, None] = "98144d45100c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
