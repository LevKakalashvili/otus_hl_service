import datetime

from fastapi import Query
from pydantic import BaseModel, Field, RootModel, field_serializer

from app.database.models import SexEnum


class UserModel(BaseModel):
    """Модель данных основной информации об пользователе"""

    id: int
    name: str
    sur_name: str | None
    birth_date: datetime.date | None
    sex: SexEnum | None
    city: str | None
    interest: str | None
    password: str | None

    class Config:
        from_attributes = True


class UserSearchRequestModel(BaseModel):
    """Модель данных для запроса на поиск пользователей"""

    name: str | None = Field(Query(default=None, example="Ива"))
    sur_name: str | None = Field(Query(default=None, example="Иван"))


class UserCreateRequestModel(BaseModel):
    """Модель данных для запроса на создание пользователя"""

    name: str = Field(...)
    sur_name: str | None = Field(default=None)
    birth_date: datetime.date | None = Field(default=None)
    sex: SexEnum | None = Field(default=None)
    city: str | None = Field(default=None)
    interest: str | None = Field(default=None)
    # password: str | None = Field(default=None)

    @field_serializer("sex")
    def serialize_group(self, sex: sex, _info):
        return sex.name.lower()

    # @field_serializer("password")
    # def serialize_group(self, password: password, _info):
    #     return password.name.lower()


class UserResponseModel(UserModel):
    id: int = Field(exclude=True)


class UserCreateResponseModel(BaseModel):
    id: int | None


class UsersResponseModel(RootModel):
    root: list[UserResponseModel]
