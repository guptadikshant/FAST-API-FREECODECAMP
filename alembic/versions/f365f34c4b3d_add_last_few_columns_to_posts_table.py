"""add last few columns to posts table

Revision ID: f365f34c4b3d
Revises: 464a80f491a4
Create Date: 2023-04-08 22:02:48.159600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f365f34c4b3d'
down_revision = '464a80f491a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(), nullable=False, server_default="TRUE"),
                  )
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
                  )


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

