"""add confirmation id from filing table

Revision ID: 3666d04f0c55
Revises: b3bfb504ae7e
Create Date: 2024-03-14 03:24:02.315715

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3666d04f0c55"
down_revision: Union[str, None] = "b3bfb504ae7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("filing", sa.Column("confirmation_id", sa.String))


def downgrade() -> None:
    op.drop_column("filing", "confirmation_id")
