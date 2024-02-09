# -*- coding: utf-8 -*-
"""
empty message.

Revision ID: adbe2344fb23
Revises:
Create Date: 2023-06-02 15:48:22.171547
"""
import sqlalchemy as sa
import sqlmodel  # added

from alembic import op

# revision identifiers, used by Alembic.
revision = "adbe2344fb23"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Account",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("userId", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("provider", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("providerAccountId", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("refresh_token", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("access_token", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("expires_at", sa.Integer(), nullable=True),
        sa.Column("token_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("scope", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("id_token", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("session_state", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider", "providerAccountId"),
    )
    op.create_table(
        "Session",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("sessionToken", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("userId", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("expires", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sessionToken"),
    )
    op.create_table(
        "User",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("emailVerified", sa.DateTime(), nullable=True),
        sa.Column("image", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("location", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "VerificationToken",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("identifier", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("token", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("expires", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("identifier", "token"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(op.f("ix_VerificationToken_id"), "VerificationToken", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_VerificationToken_id"), table_name="VerificationToken")
    op.drop_table("VerificationToken")
    op.drop_table("User")
    op.drop_table("Session")
    op.drop_table("Account")
    # ### end Alembic commands ###
