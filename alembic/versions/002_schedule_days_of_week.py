"""Replace day_of_week integer with days_of_week JSON array

Revision ID: 002
Revises: 001
Create Date: 2026-02-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column
    op.add_column("room_schedules", sa.Column("days_of_week", postgresql.JSONB(), nullable=True))

    # Migrate existing data: single int -> list, None stays None
    conn = op.get_bind()
    conn.execute(sa.text(
        "UPDATE room_schedules SET days_of_week = jsonb_build_array(day_of_week) WHERE day_of_week IS NOT NULL"
    ))

    # Drop the old column
    op.drop_column("room_schedules", "day_of_week")


def downgrade() -> None:
    op.add_column("room_schedules", sa.Column("day_of_week", sa.Integer(), nullable=True))

    # Migrate back: take first element of array
    conn = op.get_bind()
    conn.execute(sa.text(
        "UPDATE room_schedules SET day_of_week = (days_of_week->>0)::integer WHERE days_of_week IS NOT NULL AND jsonb_array_length(days_of_week) > 0"
    ))

    op.drop_column("room_schedules", "days_of_week")
