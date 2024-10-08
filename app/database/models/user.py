import datetime

from sqlalchemy import Date, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .enum import SexEnum


class User(BaseModel):
    """Таблица user"""

    __tablename__ = "user"

    name: Mapped[str] = mapped_column(
        String(255), comment="Имя пользователя", nullable=False, unique=True
    )
    sur_name: Mapped[str] = mapped_column(
        String(255), comment="Фамилия пользователя", nullable=True
    )
    birth_date: Mapped[datetime.date] = mapped_column(
        Date, comment="День рождения", nullable=True
    )
    sex: Mapped[PgEnum[SexEnum.as_list()]] = mapped_column(
        PgEnum(*SexEnum.as_list(), name="sex_enum", create_type=False),
        comment="Пол",
        nullable=True,
    )
    city: Mapped[str] = mapped_column(
        String(255), comment="Город пользователя", nullable=True
    )
    interest: Mapped[str] = mapped_column(
        String(255), comment="Интересы пользователя", nullable=True
    )
