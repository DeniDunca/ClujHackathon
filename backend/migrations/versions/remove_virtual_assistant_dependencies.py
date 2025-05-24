"""remove virtual assistant dependencies

Revision ID: remove_va_deps
Revises: a285d79fe5d5
Create Date: 2024-05-24 16:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'remove_va_deps'
down_revision = 'a285d79fe5d5'
branch_labels = None
depends_on = None


def upgrade():
    # The constraint was already dropped in a previous migration, so skip this step
    # op.drop_constraint('conversations_agent_id_fkey', 'conversations', type_='foreignkey')
    # The agent_id column was already dropped in a previous migration, so skip this step
    # op.drop_column('conversations', 'agent_id')
    # The virtual_assistants table was already dropped in a previous migration, so skip this step
    # op.drop_table('virtual_assistants')
    pass


def downgrade():
    # Recreate virtual_assistants table
    op.create_table('virtual_assistants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('capabilities', sa.String(), nullable=True),
        sa.Column('last_training_date', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Add agent_id column back to conversations
    op.add_column('conversations', sa.Column('agent_id', sa.Integer(), nullable=True))
    # Recreate the foreign key constraint
    op.create_foreign_key(
        'conversations_agent_id_fkey',
        'conversations', 'virtual_assistants',
        ['agent_id'], ['id']
    ) 