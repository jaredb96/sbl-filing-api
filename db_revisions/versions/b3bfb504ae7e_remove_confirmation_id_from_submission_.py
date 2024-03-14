"""remove confirmation id to submission table

Revision ID: b3bfb504ae7e
Revises: 8eaef8ce4c23
Create Date: 2024-03-14 03:18:39.063892

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b3bfb504ae7e"
down_revision: Union[str, None] = "8eaef8ce4c23"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("submission", "confirmation_id")


def downgrade() -> None:
    op.add_column("submission", sa.Column("confirmation_id", sa.String))
