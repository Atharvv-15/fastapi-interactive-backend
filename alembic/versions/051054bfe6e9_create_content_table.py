"""Create content table

Revision ID: 051054bfe6e9
Revises: 96531f7164f5
Create Date: 2024-10-27 14:42:25.849599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '051054bfe6e9'
down_revision: Union[str, None] = '96531f7164f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
