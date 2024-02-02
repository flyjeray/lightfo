"""02-02-add-userpost-rel

Revision ID: c2748ba51819
Revises: 435341d8a827
Create Date: 2024-02-02 10:48:34.846228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c2748ba51819'
down_revision: Union[str, None] = '435341d8a827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user-post-relations',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_index(op.f('ix_user-post-relations_post_id'), 'user-post-relations', ['post_id'], unique=False)
    op.create_index(op.f('ix_user-post-relations_user_id'), 'user-post-relations', ['user_id'], unique=False)
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_owner'), 'posts', ['owner'], unique=False)
    op.create_index(op.f('ix_posts_text'), 'posts', ['text'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)
    op.drop_constraint('posts_owner_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'user-post-relations', ['owner'], ['post_id'], ondelete='CASCADE')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_hashed_pw'), 'users', ['hashed_pw'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.drop_column('users', 'posts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('posts', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_hashed_pw'), table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_owner_fkey', 'posts', 'users', ['owner'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_text'), table_name='posts')
    op.drop_index(op.f('ix_posts_owner'), table_name='posts')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_index(op.f('ix_user-post-relations_user_id'), table_name='user-post-relations')
    op.drop_index(op.f('ix_user-post-relations_post_id'), table_name='user-post-relations')
    op.drop_table('user-post-relations')
    # ### end Alembic commands ###
