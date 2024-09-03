import datetime

from pydantic import BaseModel, Field, RootModel

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

    class Config:
        from_attributes = True


class UserCreateRequestModel(BaseModel):
    """Модель данных для запроса на создание пользователя"""

    name: str = Field(...)
    sur_name: str | None = Field(default=None)
    birth_date: datetime.date | None = Field(default=None)
    sex: SexEnum | None = Field(default=None)
    city: str | None = Field(default=None)
    interest: str | None = Field(default=None)


class UserResponseModel(UserModel):
    id: int = Field(exclude=True)


class UserCreateResponseModel(BaseModel):
    id: int | None


class UsersResponseModel(RootModel):
    root: list[UserResponseModel]
