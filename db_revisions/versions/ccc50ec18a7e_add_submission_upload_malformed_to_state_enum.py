"""add SUBMISSION_UPLOAD_MALFORMED to state enum

Revision ID: ccc50ec18a7e
Revises: 11dfc8200daa
Create Date: 2024-04-07 01:02:13.310717

"""

from typing import Sequence, Union

from alembic import op, context


# revision identifiers, used by Alembic.
revision: str = "ccc50ec18a7e"
down_revision: Union[str, None] = "fb46d55283d6"
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
    if "sqlite" not in context.get_context().dialect.name:
        op.execute("ALTER TYPE submissionstate RENAME TO submissionstate_old")
        op.execute(f"CREATE TYPE submissionstate AS ENUM{new_options}")
        op.execute("ALTER TABLE submission ALTER COLUMN state TYPE submissionstate USING state::text::submissionstate")
        op.execute("DROP TYPE submissionstate_old")


def downgrade() -> None:
    if "sqlite" not in context.get_context().dialect.name:
        op.execute("ALTER TYPE submissionstate RENAME TO submissionstate_old")
        op.execute(f"CREATE TYPE submissionstate AS ENUM{old_options}")
        op.execute("ALTER TABLE submission ALTER COLUMN state TYPE submissionstate USING state::text::submissionstate")
        op.execute("DROP TYPE submissionstate_old")
