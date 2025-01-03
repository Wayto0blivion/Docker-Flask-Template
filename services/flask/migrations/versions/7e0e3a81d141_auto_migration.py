"""Auto Migration

Revision ID: 7e0e3a81d141
Revises: a516c3c5ad4c
Create Date: 2024-12-13 15:38:40.535345

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7e0e3a81d141'
down_revision = 'a516c3c5ad4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('query_configurations',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('model_name', sa.String(length=128), nullable=False),
    sa.Column('filters', mysql.JSON(), nullable=True),
    sa.Column('columns', mysql.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('query_configurations')
    # ### end Alembic commands ###
