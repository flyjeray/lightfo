"""01-04-add-comments-table

Revision ID: b471267e64ab
Revises: 0066fe3b1afe
Create Date: 2024-04-01 21:46:33.677504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b471267e64ab'
down_revision: Union[str, None] = '0066fe3b1afe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('post', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_post'), 'comments', ['post'], unique=False)
    op.create_index(op.f('ix_comments_text'), 'comments', ['text'], unique=False)
    op.create_index(op.f('ix_comments_user'), 'comments', ['user'], unique=False)
    op.add_column('posts', sa.Column('comment_amount', sa.Integer(), nullable=False, server_default='0'))
    op.create_index(op.f('ix_posts_comment_amount'), 'posts', ['comment_amount'], unique=False)
    op.add_column('users', sa.Column('comment_amount', sa.Integer(), nullable=False, server_default='0'))
    op.create_index(op.f('ix_users_comment_amount'), 'users', ['comment_amount'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_comment_amount'), table_name='users')
    op.drop_column('users', 'comment_amount')
    op.drop_index(op.f('ix_posts_comment_amount'), table_name='posts')
    op.drop_column('posts', 'comment_amount')
    op.drop_index(op.f('ix_comments_user'), table_name='comments')
    op.drop_index(op.f('ix_comments_text'), table_name='comments')
    op.drop_index(op.f('ix_comments_post'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###