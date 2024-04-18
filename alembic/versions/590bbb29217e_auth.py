"""Auth

Revision ID: 590bbb29217e
Revises:
Create Date: 2024-04-18 12:30:13.598477

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "590bbb29217e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  # ### commands auto generated by Alembic - please adjust! ###
  op.create_table(
    "books",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("title", sa.String(), nullable=True),
    sa.Column("author", sa.String(), nullable=True),
    sa.Column("category", sa.String(), nullable=True),
    sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(op.f("ix_books_author"), "books", ["author"], unique=False)
  op.create_index(op.f("ix_books_category"), "books", ["category"], unique=False)
  op.create_index(op.f("ix_books_id"), "books", ["id"], unique=False)
  op.create_index(op.f("ix_books_title"), "books", ["title"], unique=False)
  op.create_table(
    "roles",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=True),
    sa.Column("name", sa.String(length=450), nullable=False),
    sa.Column("status", sa.Boolean(), nullable=True),
    sa.Column("created_at", sa.DateTime(), nullable=True),
    sa.Column("updated_at", sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint("id", "name"),
  )
  op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=True)
  op.create_table(
    "tokens",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=True),
    sa.Column("token", sa.String(), nullable=True),
    sa.Column("status", sa.Boolean(), nullable=True),
    sa.Column("created_at", sa.DateTime(), nullable=True),
    sa.Column("updated_at", sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(op.f("ix_tokens_id"), "tokens", ["id"], unique=True)
  op.create_table(
    "users",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("role_id", sa.Integer(), nullable=True),
    sa.Column("full_name", sa.String(), nullable=True),
    sa.Column("email", sa.String(), nullable=True),
    sa.Column("password", sa.String(), nullable=True),
    sa.Column("avatar", sa.String(), nullable=True),
    sa.Column("is_active", sa.Boolean(), nullable=True),
    sa.Column("is_email_verified", sa.Boolean(), nullable=True),
    sa.Column("email_verified_at", sa.DateTime(), nullable=True),
    sa.Column("created_at", sa.DateTime(), nullable=True),
    sa.Column("updated_at", sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="SET NULL"),
    sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(op.f("ix_users_id"), "users", ["id"], unique=True)
  # ### end Alembic commands ###


def downgrade() -> None:
  # ### commands auto generated by Alembic - please adjust! ###
  op.drop_index(op.f("ix_users_id"), table_name="users")
  op.drop_table("users")
  op.drop_index(op.f("ix_tokens_id"), table_name="tokens")
  op.drop_table("tokens")
  op.drop_index(op.f("ix_roles_id"), table_name="roles")
  op.drop_table("roles")
  op.drop_index(op.f("ix_books_title"), table_name="books")
  op.drop_index(op.f("ix_books_id"), table_name="books")
  op.drop_index(op.f("ix_books_category"), table_name="books")
  op.drop_index(op.f("ix_books_author"), table_name="books")
  op.drop_table("books")
  # ### end Alembic commands ###