"""Added unite

Revision ID: 5837f9c91ee2
Revises: 3be5d7e6337f
Create Date: 2023-08-21 16:37:52.035547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5837f9c91ee2'
down_revision = '3be5d7e6337f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredient', sa.Column('unite', sa.String(length=32), nullable=True))
    op.alter_column('ingredient', 'name',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('ingredient', 'categorie',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.create_index(op.f('ix_ingredient_unite'), 'ingredient', ['unite'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ingredient_unite'), table_name='ingredient')
    op.alter_column('ingredient', 'categorie',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('ingredient', 'name',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.drop_column('ingredient', 'unite')
    # ### end Alembic commands ###
