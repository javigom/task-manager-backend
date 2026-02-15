"""initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-13 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey(
            'users.id'), nullable=False),
    )

    op.create_table(
        'task_participants',
        sa.Column('task_id', sa.Integer(), sa.ForeignKey(
            'tasks.id'), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey(
            'users.id'), primary_key=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('task_participants')
    op.drop_table('tasks')
    op.drop_table('users')
