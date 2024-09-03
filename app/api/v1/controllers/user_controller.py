from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.models import UserCreateRequestModel, UserModel
from app.core.based import BaseController
from app.database.db import get_session
from app.database.models import User


class UserController(BaseController):
    model = f'"{User.__tablename__}"'

    @staticmethod
    async def create_user(
        user_info: UserCreateRequestModel, session: AsyncSession = Depends(get_session)
    ) -> int:
        """Метод создания пользователя"""
        id_ = await UserController.create(
            session=session,
            model=UserController.model,
            data=user_info.model_dump(exclude_none=True),
        )
        return id_

    @staticmethod
    async def get_user_info(
        user_id: int, session: AsyncSession = Depends(get_session)
    ) -> UserModel:
        """Метод получения информации о пользователе по его ид"""
        info = await UserController.get_by_id(
            session=session, id_=user_id, model=UserController.model
        )
        return UserModel.model_validate(info)

    @staticmethod
    async def get_all_users_info(
        session: AsyncSession = Depends(get_session),
    ) -> list[UserModel]:
        """Метод получения информации о всех пользователях"""
        info = await UserController.get_all(session=session, model=UserController.model)
        return [UserModel.model_validate(element) for element in info]
