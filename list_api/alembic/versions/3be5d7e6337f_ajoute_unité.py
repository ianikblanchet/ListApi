"""ajoute unité

Revision ID: 3be5d7e6337f
Revises: 4b62ed9ec579
Create Date: 2023-08-21 16:16:10.399879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3be5d7e6337f'
down_revision = '4b62ed9ec579'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('ingredient', sa.Column('unite', sa.string(32), index=True))


def downgrade() :
    op.drop_column('ingredient', 'unite')
