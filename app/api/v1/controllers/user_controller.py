from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.models import UserCreateRequestModel, UserModel
from app.api.v1.models.user_model import UserSearchRequestModel
from app.core.based import BaseController
from app.core.models.common import BasePaginationParams
from app.database.db import get_session
from app.database.models import User


class UserController(BaseController):
    model = f'"{User.__tablename__}"'

    @staticmethod
    async def search_users_info(
        user_info: UserSearchRequestModel = Depends(),
        sessions: List[AsyncSession] = Depends(get_session),
        pagination: BasePaginationParams = Depends(),
    ) -> list[UserModel]:
        """Метод поиск пользователей"""
        info = await UserController.search(
            sessions=sessions,
            model=UserController.model,
            data=user_info.model_dump(exclude_none=True),
            pagination=pagination,
        )
        return [UserModel.model_validate(element) for element in info]

    @staticmethod
    async def create_user(
        user_info: UserCreateRequestModel,
        sessions: List[AsyncSession] = Depends(get_session),
    ) -> int:
        """Метод создания пользователя"""
        id_ = await UserController.create(
            sessions=sessions,
            model=UserController.model,
            data=user_info.model_dump(exclude_none=True),
        )
        return id_

    @staticmethod
    async def get_user_info(
        user_id: int, sessions: List[AsyncSession] = Depends(get_session)
    ) -> UserModel:
        """Метод получения информации о пользователе по его id"""
        info = await UserController.get_by_id(
            sessions=sessions, id_=user_id, model=UserController.model
        )
        return UserModel.model_validate(info)

    @staticmethod
    async def get_all_users_info(
        sessions: List[AsyncSession] = Depends(get_session),
        pagination: BasePaginationParams = Depends(),
    ) -> list[UserModel]:
        """Метод получения информации о всех пользователях"""
        info = await UserController.get_all(
            sessions=sessions, model=UserController.model, pagination=pagination
        )
        return [UserModel.model_validate(element) for element in info]
