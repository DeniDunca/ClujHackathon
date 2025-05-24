"""add patient_id to messages

Revision ID: add_patient_id
Revises: remove_va_deps
Create Date: 2024-05-24 16:55:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_patient_id'
down_revision = 'remove_va_deps'
branch_labels = None
depends_on = None

def upgrade():
    # Add patient_id column to messages table
    op.add_column('messages', sa.Column('patient_id', sa.Integer(), nullable=True))
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_patient_id',
        'messages', 'users',
        ['patient_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # Drop foreign key constraint
    op.drop_constraint('fk_patient_id', 'messages', type_='foreignkey')
    # Drop patient_id column
    op.drop_column('messages', 'patient_id') 