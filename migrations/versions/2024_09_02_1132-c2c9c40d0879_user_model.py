"""user model

Revision ID: c2c9c40d0879
Revises: 
Create Date: 2024-09-02 11:32:07.657145

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c2c9c40d0879"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum("male", "female", name="sex_enum").create(op.get_bind())
    op.create_table(
        "user",
        sa.Column(
            "name", sa.String(length=255), nullable=False, comment="Иям пользователя"
        ),
        sa.Column(
            "sur_name",
            sa.String(length=255),
            nullable=True,
            comment="Фамилия пользователя",
        ),
        sa.Column("birth_date", sa.Date(), nullable=True, comment="День рождения"),
        sa.Column(
            "sex",
            postgresql.ENUM("male", "female", name="sex_enum", create_type=False),
            nullable=True,
            comment="Пол",
        ),
        sa.Column(
            "city", sa.String(length=255), nullable=True, comment="Город пользователя"
        ),
        sa.Column(
            "interest",
            sa.String(length=255),
            nullable=True,
            comment="Интересы пользователя",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment="Уникальный идентификатор объекта",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    sa.Enum("male", "female", name="sex_enum").drop(op.get_bind())
    # ### end Alembic commands ###
