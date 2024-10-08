import uuid

from fastapi import status
from pydantic import BaseModel, Field

from app.enums.response import ResponseCode


class BaseResponseErrorModel(BaseModel):
    uuid: uuid.UUID
    message: str
    status: str = "Error"


NotFoundResponse = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found Error",
    }
}


BadRequestResponse = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
    }
}


class BaseResponse(BaseModel):
    """Базовая схема ответа"""

    code: ResponseCode = Field(
        default=ResponseCode.OK, description="Код ответа (0 - в случае успеха)"
    )
    data: dict = Field(default={}, description="Вложенные данные")
    error_text: str = Field(default="", description="Текст ошибки")
