"""change submission enum

Revision ID: 7a1b7eab0167
Revises: 8eaef8ce4c23
Create Date: 2024-03-13 14:38:34.324557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a1b7eab0167"
down_revision: Union[str, None] = "8eaef8ce4c23"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("submission", "state")
    op.add_column(
        "submission",
        sa.Column(
            "state",
            sa.Enum(
                "SUBMISSION_UPLOADED",
                "VALIDATION_IN_PROGRESS",
                "VALIDATION_WITH_ERRORS",
                "VALIDATION_WITH_WARNINGS",
                "VALIDATION_SUCCESSFUL",
                "SUBMISSION_CERTIFIED",
                name="submissionstate",
            ),
        ),
    )


def downgrade() -> None:
    op.drop_column("submission", "state")
    op.add_column(
        "submission",
        sa.Column(
            "state",
            sa.Enum(
                "SUBMISSION_UPLOADED",
                "VALIDATION_IN_PROGRESS",
                "VALIDATION_WITH_ERRORS",
                "VALIDATION_WITH_WARNINGS",
                "VALIDATION_SUCCESSFUL",
                "SUBMISSION_SIGNED",
                name="submissionstate",
            ),
        ),
    )
