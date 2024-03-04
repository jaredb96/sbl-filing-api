"""240304 change filing_task_state to filing_task_progress

Revision ID: bbc51b08d22f
Revises: 19fccbf914bc
Create Date: 2024-03-04 12:02:27.253888

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "bbc51b08d22f"
down_revision: Union[str, None] = "19fccbf914bc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("filing_task_state", "filing_task_progress")


def downgrade() -> None:
    op.rename_table("filing_task_progress", "filing_task_state")
