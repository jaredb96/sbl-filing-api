"""create validation_result table

Revision ID: 652b29a8d810
Revises: f30c5c3c7a42
Create Date: 2023-12-12 12:45:21.895903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db_revisions.utils import table_exists

# revision identifiers, used by Alembic.
revision: str = "652b29a8d810"
down_revision: Union[str, None] = "f30c5c3c7a42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("validation_result"):
        op.create_table(
            "validation_result",
            sa.Column("id", sa.Integer, nullable=False),
            sa.Column("submission_id", sa.String, nullable=False),
            sa.Column("validation_id", sa.String, nullable=False),
            sa.Column("field_name", sa.String, nullable=False),
            sa.Column("severity", sa.String, nullable=False),
            sa.Column("event_time", sa.DateTime, server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.ForeignKeyConstraint(
                ["submission_id"],
                ["submission.submission_id"],
            ),
        )


def downgrade() -> None:
    op.drop_table("validation_result")
