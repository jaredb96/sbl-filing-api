"""make filing institution_snapshot_id nullable

Revision ID: dcafabe9141e
Revises: ffd779216f6d
Create Date: 2024-04-08 18:57:04.957822

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "dcafabe9141e"
down_revision: Union[str, None] = "fb46d55283d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("filing", schema=None) as batch_op:
        batch_op.alter_column("institution_snapshot_id", existing_nullable=False, nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("filing", schema=None) as batch_op:
        batch_op.alter_column("institution_snapshot_id", existing_nullable=True, nullable=False)
