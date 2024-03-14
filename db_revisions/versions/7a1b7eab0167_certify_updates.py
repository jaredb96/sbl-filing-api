"""certify updates

Revision ID: 7a1b7eab0167
Revises: b3bfb504ae7e
Create Date: 2024-03-13 14:38:34.324557

"""
from typing import Sequence, Union

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a1b7eab0167"
down_revision: Union[str, None] = "b3bfb504ae7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


old_options = (
    'SUBMISSION_SIGNED',
    'SUBMISSION_STARTED',
    'SUBMISSION_UPLOADED',
    'VALIDATION_IN_PROGRESS',
    'VALIDATION_WITH_ERRORS',
    'VALIDATION_WITH_WARNINGS',
    'VALIDATION_SUCCESSFUL',
)
new_options = (
    'SUBMISSION_CERTIFIED',
    'SUBMISSION_STARTED',
    'SUBMISSION_UPLOADED',
    'VALIDATION_IN_PROGRESS',
    'VALIDATION_WITH_ERRORS',
    'VALIDATION_WITH_WARNINGS',
    'VALIDATION_SUCCESSFUL',
)


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
