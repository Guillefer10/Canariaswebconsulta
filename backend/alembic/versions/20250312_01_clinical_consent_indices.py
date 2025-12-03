"""Add clinical tables and consent records and indices

Revision ID: 20250312_01
Revises:
Create Date: 2025-03-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20250312_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clinicalepisode",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["client_id"], ["clientprofile.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "consentrecord",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("consent_type", sa.Enum("privacy_policy", "health_data", name="consenttype"), nullable=False),
        sa.Column("text_version", sa.String(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column("accepted_by_user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["accepted_by_user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["client_id"], ["clientprofile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "clinicalnote",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("worker_id", sa.Integer(), nullable=False),
        sa.Column("episode_id", sa.Integer(), nullable=True),
        sa.Column("appointment_id", sa.Integer(), nullable=True),
        sa.Column("treatment_type_id", sa.Integer(), nullable=True),
        sa.Column("note_date", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("motive", sa.String(), nullable=True),
        sa.Column("observations", sa.Text(), nullable=True),
        sa.Column("plan", sa.Text(), nullable=True),
        sa.Column("attachments", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointment.id"]),
        sa.ForeignKeyConstraint(["client_id"], ["clientprofile.id"]),
        sa.ForeignKeyConstraint(["episode_id"], ["clinicalepisode.id"]),
        sa.ForeignKeyConstraint(["treatment_type_id"], ["treatmenttype.id"]),
        sa.ForeignKeyConstraint(["worker_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_appointment_worker_start", "appointment", ["worker_id", "start_datetime"], unique=False)
    op.create_index("ix_appointment_client_start", "appointment", ["client_id", "start_datetime"], unique=False)

    op.create_index("ix_session_client_performed", "treatmentsession", ["client_id", "performed_at"], unique=False)
    op.create_index("ix_session_worker_performed", "treatmentsession", ["worker_id", "performed_at"], unique=False)

    op.create_index("ix_consent_client_type", "consentrecord", ["client_id", "consent_type"], unique=False)
    op.create_index("ix_clinical_note_client_date", "clinicalnote", ["client_id", "note_date"], unique=False)
    op.create_index("ix_clinical_note_episode", "clinicalnote", ["episode_id"], unique=False)
    op.create_index("ix_clinical_episode_client_active", "clinicalepisode", ["client_id", "is_active"], unique=False)
    op.create_index("ix_clinical_episode_start", "clinicalepisode", ["started_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_clinical_episode_start", table_name="clinicalepisode")
    op.drop_index("ix_clinical_episode_client_active", table_name="clinicalepisode")
    op.drop_index("ix_clinical_note_episode", table_name="clinicalnote")
    op.drop_index("ix_clinical_note_client_date", table_name="clinicalnote")
    op.drop_index("ix_consent_client_type", table_name="consentrecord")
    op.drop_index("ix_session_worker_performed", table_name="treatmentsession")
    op.drop_index("ix_session_client_performed", table_name="treatmentsession")
    op.drop_index("ix_appointment_client_start", table_name="appointment")
    op.drop_index("ix_appointment_worker_start", table_name="appointment")
    op.drop_table("clinicalnote")
    op.drop_table("consentrecord")
    op.drop_table("clinicalepisode")
