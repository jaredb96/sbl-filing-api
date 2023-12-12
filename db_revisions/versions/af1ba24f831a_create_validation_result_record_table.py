"""create validation_result_record table

Revision ID: af1ba24f831a
Revises: 652b29a8d810
Create Date: 2023-12-12 12:45:28.115794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db_revisions.utils import table_exists

# revision identifiers, used by Alembic.
revision: str = 'af1ba24f831a'
down_revision: Union[str, None] = '652b29a8d810'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("validation_result_record"):
        op.create_table(
            "validation_result_record",
            sa.Column("id", sa.Integer, nullable=False),
            sa.Column("result_id", sa.Integer, nullable=False),
            sa.Column("record", sa.Integer, nullable=False),
            sa.Column("data", sa.String),
            sa.Column("event_time", sa.DateTime, server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.ForeignKeyConstraint(
                ["result_id"],
                ["validation_result.id"],
            ),
        )


def downgrade() -> None:
    op.drop_table("validation_result_record")