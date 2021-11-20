"""create_user_table

Revision ID: 807e52aefcad
Revises: 4b943bb2a553
Create Date: 2021-11-19 19:28:50.681017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '807e52aefcad'
down_revision = '4b943bb2a553'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
