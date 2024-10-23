import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.core.settings import Settings
from app.database.db import get_session

health_check_router = APIRouter(tags=["Health Checks"])


@health_check_router.get(
    "/", summary="Метод выполняет запрос на вывод текущей даты и времени"
)
async def get_datetime() -> Any:
    return Response(
        content=f"Time: {datetime.datetime.now(datetime.timezone.utc).isoformat()}"
    )


@health_check_router.get(
    "/checks/liveness", summary="Метод выполняет проверку работоспособности приложения"
)
def liveness(settings: Settings) -> Any:
    return {
        "status": HTTP_200_OK,
        "name": settings.SERVICE,
        "description": settings.PROJECT_DESCRIPTION,
        "environment": settings.ENVIRONMENT,
    }


@health_check_router.get(
    "/checks/readiness",
    summary="Метод выполняет обращения в подсистемы, с которыми работает",
)
async def readiness(sessions: List[AsyncSession] = Depends(get_session)) -> Any:
    try:
        statistics_ms = await sessions[0].scalar(text("SELECT version()"))
        return {
            "Status": HTTP_200_OK,
            "DB version": statistics_ms,
        }

    except Exception as e:
        return {"status": HTTP_503_SERVICE_UNAVAILABLE, "error": str(e)}


@health_check_router.get("/checks/version", summary="Возвращает хэш версии")
def version(settings: Settings) -> Any:
    return {"Хеш версии": hash(settings.PROJECT_VERSION)}
