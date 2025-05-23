"""scores type from int to string

Revision ID: 4c8993720d9a
Revises: 3c3c6e5bd61c
Create Date: 2025-02-26 14:37:32.654414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c8993720d9a'
down_revision: Union[str, None] = '3c3c6e5bd61c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coefficients', 'curr_quarter')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coefficients', sa.Column('curr_quarter', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
