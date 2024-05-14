"""add published and created_at columns

Revision ID: 9489c8236867
Revises: 365f56bc5394
Create Date: 2024-05-14 15:40:46.882979

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9489c8236867"
down_revision: Union[str, None] = "365f56bc5394"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("is_published", sa.Boolean, nullable=False, server_default="true"))
    op.add_column(
        "posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )


def downgrade() -> None:
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "created_at")
