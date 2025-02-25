"""Fix ForeignKey reference in Expense model

Revision ID: ea92bbabfb42
Revises: bce2e855196a
Create Date: 2024-12-04 17:42:21.942208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea92bbabfb42'
down_revision = 'bce2e855196a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('expense_date', sa.DateTime(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('expense_type', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    # ### end Alembic commands ###
