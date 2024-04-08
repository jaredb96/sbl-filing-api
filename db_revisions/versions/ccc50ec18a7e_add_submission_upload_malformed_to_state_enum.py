"""add SUBMISSION_UPLOAD_MALFORMED to state enum

Revision ID: ccc50ec18a7e
Revises: 11dfc8200daa
Create Date: 2024-04-07 01:02:13.310717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ccc50ec18a7e"
down_revision: Union[str, None] = "ffd779216f6d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


old_options = (
    "SUBMISSION_UPLOADED",
    "VALIDATION_IN_PROGRESS",
    "VALIDATION_WITH_ERRORS",
    "VALIDATION_WITH_WARNINGS",
    "VALIDATION_SUCCESSFUL",
    "SUBMISSION_ACCEPTED",
    "SUBMISSION_STARTED",
)
new_options = sorted(old_options + ("SUBMISSION_UPLOAD_MALFORMED",))


def upgrade() -> None:
    with op.batch_alter_table("submission", schema=None) as batch_op:
        batch_op.alter_column(
            "state",
            type_=sa.Enum(*new_options, name="submissionstate"),
            existing_type=sa.Enum(*old_options, name="submissionstate"),
            existing_server_default=sa.text("'text'"),
        )


def downgrade() -> None:
    with op.batch_alter_table("submission", schema=None) as batch_op:
        batch_op.alter_column(
            "state",
            type_=sa.Enum(*old_options, name="submissionstate"),
            existing_type=sa.Enum(*new_options, name="submissionstate"),
            existing_server_default=sa.text("'text'"),
        )
