"""empty message

Revision ID: 2461fed06317
Revises: b02ae5c78a9b
Create Date: 2022-06-22 18:33:54.744962

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2461fed06317'
down_revision = 'b02ae5c78a9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('tags', sa.String(length=250), nullable=True))
    op.create_unique_constraint(None, 'posts', ['tags'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='unique')
    op.drop_column('posts', 'tags')
    # ### end Alembic commands ###
