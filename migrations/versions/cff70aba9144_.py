"""empty message

Revision ID: cff70aba9144
Revises: 388f24be9a1b
Create Date: 2020-10-22 13:49:17.558592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cff70aba9144'
down_revision = '388f24be9a1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('keywords', 'keyword',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'keywords', ['keyword'])
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'keywords', type_='unique')
    op.alter_column('keywords', 'keyword',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###