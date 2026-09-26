"""Day 5 audit logs"""
from alembic import op
import sqlalchemy as sa
revision="6d5f0b4e2c11"; down_revision="525ffa94d7cd"; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("audit_logs",
        sa.Column("id",sa.String(),nullable=False),
        sa.Column("actor_id",sa.String(),nullable=True),
        sa.Column("action",sa.String(),nullable=False),
        sa.Column("entity_type",sa.String(),nullable=False),
        sa.Column("entity_id",sa.String(),nullable=False),
        sa.Column("details",sa.String(),nullable=True),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=True),
        sa.ForeignKeyConstraint(["actor_id"],["users.id"]),
        sa.PrimaryKeyConstraint("id"))
def downgrade(): op.drop_table("audit_logs")
