"""create posts table

Revision ID: 98144d45100c
Revises: 
Create Date: 2024-05-14 14:55:35.613099

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "98144d45100c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
