"""remove acccepter from and add submitter_name and submitter_email to submission table

Revision ID: d0ab7f051052
Revises: 7a1b7eab0167
Create Date: 2024-03-27 15:58:16.294508

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d0ab7f051052"
down_revision: Union[str, None] = "7a1b7eab0167"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("submission") as batch_op:
        batch_op.drop_column("accepter")
        batch_op.add_column(sa.Column("submitter_name", sa.String, nullable=True))
        batch_op.add_column(sa.Column("submitter_email", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("submission", "submitter_name")
    op.drop_column("submission", "submitter_email")
    op.add_column("submission", sa.Column("accepter", sa.String, nullable=True))
