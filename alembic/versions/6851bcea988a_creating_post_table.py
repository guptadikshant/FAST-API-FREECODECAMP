"""creating post table

Revision ID: 6851bcea988a
Revises: 
Create Date: 2023-04-08 18:38:49.345910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6851bcea988a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('title', sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
