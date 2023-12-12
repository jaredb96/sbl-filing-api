"""create submission tables

Revision ID: f30c5c3c7a42
Revises: 
Create Date: 2023-12-12 12:40:14.501180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db_revisions.utils import table_exists


# revision identifiers, used by Alembic.
revision: str = "f30c5c3c7a42"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("submission"):
        op.create_table(
            "submission",
            sa.Column("submission_id", sa.String, nullable=False),
            sa.Column("submitter", sa.String, nullable=False),
            sa.Column("lei", sa.String, nullable=False),
            sa.Column("json_dump", sa.JSON),
            sa.Column("event_time", sa.DateTime, server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("submission_id"),
        )


def downgrade() -> None:
    op.drop_table("submission")
