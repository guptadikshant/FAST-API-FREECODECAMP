"""add content column to post table

Revision ID: 1aeea805626b
Revises: 6851bcea988a
Create Date: 2023-04-08 18:45:15.694086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aeea805626b'
down_revision = '6851bcea988a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
