"""add_content_column_to_posts_table

Revision ID: 4b943bb2a553
Revises: 07c587107d2d
Create Date: 2021-11-19 19:22:41.215502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b943bb2a553'
down_revision = '07c587107d2d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
