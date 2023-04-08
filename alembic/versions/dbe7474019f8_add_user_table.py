"""add user table

Revision ID: dbe7474019f8
Revises: 1aeea805626b
Create Date: 2023-04-08 18:49:08.473512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbe7474019f8'
down_revision = '1aeea805626b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email',sa.String(), nullable=False),
        sa.Column('password',sa.String(), nullable=False),
        sa.Column('create_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()') ,nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
