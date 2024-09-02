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


class UserRequestModel(BaseModel):
    """Модель данных для запроса основной информации об пользователе"""

    ...


class UserResponseModel(UserModel):
    id: int = Field(exclude=True)


class UsersResponseModel(RootModel):
    root: list[UserResponseModel]
