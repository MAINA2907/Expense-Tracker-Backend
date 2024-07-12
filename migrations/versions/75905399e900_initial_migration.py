"""initial migration

Revision ID: 75905399e900
Revises: 
Create Date: 2024-07-12 18:20:05.527938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75905399e900'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('budget_name', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_budget_user_id_user')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense_name', sa.String(), nullable=True),
    sa.Column('expense_amount', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('paymode', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_expense_user_id_user')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expenses_categories',
    sa.Column('expense_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('fk_expenses_categories_category_id_category')),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], name=op.f('fk_expenses_categories_expense_id_expense')),
    sa.PrimaryKeyConstraint('expense_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expenses_categories')
    op.drop_table('expense')
    op.drop_table('budget')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###