from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="Уникальный идентификатор объекта",
    )

    def as_dict(self, exclude: set = None):
        if not exclude:
            exclude = set()
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }

    def as_dict_lower(self, exclude: set = None):
        if not exclude:
            exclude = set()
        return {
            str.lower(c.name): getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }
