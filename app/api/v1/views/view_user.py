from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.controllers import UserController
from app.api.v1.models import (
    UserCreateResponseModel,
    UserModel,
    UserResponseModel,
    UsersResponseModel,
)
from app.core.based import NotFoundResponse

user_router = APIRouter(
    tags=["Пользователи"],
    prefix="/user",
)


@user_router.post(
    "/login",
    responses=NotFoundResponse,
    summary="Регистрация пользователя",
)
async def login_user() -> dict:
    #     info: Annotated[
    #         UserModel,
    #         Depends(UserController.get_user_info),
    #     ]
    # ) -> UserResponseModel:
    #     response = UserResponseModel.model_validate(info)
    #     return response
    # TODO: дописать регистрацию
    return {}


@user_router.get(
    "/search",
    responses=NotFoundResponse,
    summary="Поиск пользователя по имени и фамилии",
)
async def search_user_info(
    info: Annotated[
        list[UserModel],
        Depends(UserController.search_users_info),
    ]
) -> UsersResponseModel:
    return UsersResponseModel.model_validate(
        [UserResponseModel.model_validate(element) for element in info]
    )


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
    "",
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


@user_router.post(
    "",
    responses=NotFoundResponse,
    summary="Создание пользователя",
)
async def create_user_info(
    id_: Annotated[
        int,
        Depends(UserController.create_user),
    ]
) -> UserCreateResponseModel:
    return UserCreateResponseModel(id=id_)
