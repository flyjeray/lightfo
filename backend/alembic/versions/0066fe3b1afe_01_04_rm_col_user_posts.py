"""01-04-rm-col-user-posts

Revision ID: 0066fe3b1afe
Revises: 2709a134b8ec
Create Date: 2024-04-01 20:34:54.262495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0066fe3b1afe'
down_revision: Union[str, None] = '2709a134b8ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_posts', table_name='users')
    op.drop_column('users', 'posts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('posts', postgresql.ARRAY(sa.INTEGER()), server_default=sa.text("'{}'::integer[]"), autoincrement=False, nullable=True))
    op.create_index('ix_users_posts', 'users', ['posts'], unique=False)
    # ### end Alembic commands ###
