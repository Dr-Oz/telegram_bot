"""initial migration

Revision ID: 994ff0402a8c
Revises: 
Create Date: 2023-01-15 13:30:02.728280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '994ff0402a8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_code', sa.VARCHAR(length=255), nullable=True),
    sa.Column('category_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('subcategory_code', sa.VARCHAR(length=255), nullable=True),
    sa.Column('subcategory_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('photo', sa.VARCHAR(length=255), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    # ### end Alembic commands ###
