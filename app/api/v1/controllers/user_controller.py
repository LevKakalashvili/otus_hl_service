from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.models import UserModel
from app.core.based import BaseController
from app.database.db import get_session
from app.database.models import User


class UserController(BaseController):
    model = UserModel

    @staticmethod
    async def get_user_info(
        user_id: int, session: AsyncSession = Depends(get_session)
    ) -> UserModel:
        info = await UserController.get_by_id(
            session=session, id=user_id, model=f'"{User.__tablename__}"'
        )
        return UserModel.model_validate(info)

    @staticmethod
    async def get_all_users_info(
        session: AsyncSession = Depends(get_session),
    ) -> list[UserModel]:
        info = await UserController.get_all(
            session=session, model=f'"{User.__tablename__}"'
        )
        return [UserModel.model_validate(element) for element in info]
