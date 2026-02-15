"""add timestamps to users and tasks

Revision ID: 0002_add_timestamps
Revises: 0001_initial
Create Date: 2026-02-14 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '0002_add_timestamps'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add timestamps to users table
    op.add_column('users', sa.Column('created_at', sa.DateTime(
        timezone=True), server_default=func.now(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(
        timezone=True), server_default=func.now(), nullable=False))

    # Add timestamps to tasks table
    op.add_column('tasks', sa.Column('created_at', sa.DateTime(
        timezone=True), server_default=func.now(), nullable=False))
    op.add_column('tasks', sa.Column('updated_at', sa.DateTime(
        timezone=True), server_default=func.now(), nullable=False))


def downgrade() -> None:
    # Remove timestamps from tasks table
    op.drop_column('tasks', 'updated_at')
    op.drop_column('tasks', 'created_at')

    # Remove timestamps from users table
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
