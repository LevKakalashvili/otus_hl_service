from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.controllers import UserController
from app.api.v1.models import UserModel, UserResponseModel, UsersResponseModel
from app.core.based import NotFoundResponse

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.get(
    "/{user_id}",
    responses=NotFoundResponse,
    summary="Запрос информации о пользователе",
)
async def get_user_info(
    info: Annotated[
        UserModel,
        Depends(UserController.get_user_info),
    ]
) -> UserResponseModel:
    response = UserResponseModel.model_validate(info)
    return response


@user_router.get(
    "/",
    responses=NotFoundResponse,
    summary="Запрос информации о всех пользователях",
)
async def get_all_user_info(
    info: Annotated[
        list[UserModel],
        Depends(UserController.get_all_users_info),
    ]
) -> UsersResponseModel:
    return UsersResponseModel.model_validate(
        [UserResponseModel.model_validate(element) for element in info]
    )
