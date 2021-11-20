"""add_foreignkey_to_posts_table

Revision ID: 47db29ae732c
Revises: 807e52aefcad
Create Date: 2021-11-19 19:35:49.359086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47db29ae732c'
down_revision = '807e52aefcad'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],
                            remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
