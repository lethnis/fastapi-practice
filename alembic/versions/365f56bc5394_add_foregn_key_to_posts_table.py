"""add foregn-key to posts table

Revision ID: 365f56bc5394
Revises: 9bf1c0471c46
Create Date: 2024-05-14 15:35:44.147923

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "365f56bc5394"
down_revision: Union[str, None] = "9bf1c0471c46"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "posts_users_fk", "posts", "users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
