"""add user role column

Revision ID: 20260316_01
Revises:
Create Date: 2026-03-16
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260316_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if not insp.has_table("users"):
        return
    if any(c["name"] == "role" for c in insp.get_columns("users")):
        return
    op.add_column("users", sa.Column("role", sa.String(length=20), server_default="user", nullable=False))


def downgrade() -> None:
    op.drop_column("users", "role")