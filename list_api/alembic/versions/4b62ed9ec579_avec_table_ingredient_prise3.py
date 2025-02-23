"""avec table ingredient prise3

Revision ID: 4b62ed9ec579
Revises: ac6d0c76e229
Create Date: 2023-08-21 08:21:02.838030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b62ed9ec579'
down_revision = 'ac6d0c76e229'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ingredient',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(32), nullable=False, index=True),
        sa.Column('categorie', sa.String(32), nullable=False, index=True),
    )


def downgrade():
    op.drop_table('ingredient')
