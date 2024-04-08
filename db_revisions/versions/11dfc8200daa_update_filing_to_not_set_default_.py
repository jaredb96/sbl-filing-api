"""update Filing to not set default institution_snapshot_id

Revision ID: 11dfc8200daa
Revises: ffd779216f6d
Create Date: 2024-04-06 02:50:01.197728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11dfc8200daa'
down_revision: Union[str, None] = 'ffd779216f6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
