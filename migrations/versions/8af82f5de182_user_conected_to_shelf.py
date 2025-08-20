"""User conected to shelf

Revision ID: 8af82f5de182
Revises: 5a84166042a4
Create Date: 2025-08-13 22:28:28.631918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8af82f5de182'
down_revision: Union[str, Sequence[str], None] = '5a84166042a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('shelves', sa.Column('user_id', sa.Integer(), nullable=True))

    op.execute("UPDATE shelves SET user_id = 1 WHERE user_id IS NULL")


    op.alter_column('shelves', 'user_id', nullable=False)

    # Create foreign key constraint
    op.create_foreign_key(
        'fk_shelves_user_id_users',
        'shelves', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint('fk_shelves_user_id_users', 'shelves', type_='foreignkey')

    #
    op.drop_column('shelves', 'user_id')