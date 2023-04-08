"""add foreign key to posts table

Revision ID: 464a80f491a4
Revises: dbe7474019f8
Create Date: 2023-04-08 19:02:04.864894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464a80f491a4'
down_revision = 'dbe7474019f8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE'
                          )


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('owner_id')