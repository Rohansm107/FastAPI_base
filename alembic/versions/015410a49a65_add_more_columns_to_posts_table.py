"""add_more_columns_to_posts_table

Revision ID: 015410a49a65
Revises: 47db29ae732c
Create Date: 2021-11-19 19:42:51.377300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '015410a49a65'
down_revision = '47db29ae732c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
