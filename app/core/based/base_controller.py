from typing import List

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.common import BasePaginationParams
from app.core.settings import settings


class BaseController:
    """
    Базовый контроллер
    """

    @staticmethod
    async def create(
        sessions: List[AsyncSession],
        model: str,
        data: dict,
    ) -> int:
        if isinstance(data, dict) and data:
            query = (
                f"INSERT INTO {model} ("
                + ", ".join(['"' + key_ + '"' for key_ in data.keys()])
                + ") VALUES ("
                + ", ".join("'" + str(value) + "'" for value in data.values())
                + ") RETURNING id"
            )
            logger.debug(query)
            try:
                session = sessions[settings.DB_MASTER_INDEX]
                logger.debug(str(session.bind.url))
                item = await session.execute(text(query))
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=e.args[0],
                )
        return list(item)[0][0]

    @staticmethod
    async def get_by_id(
        sessions: List[AsyncSession],
        model: str,
        id_: int,
        detail_by_not_fount: str = "Not found.",
    ) -> object:
        query = f"SELECT * FROM {model} WHERE id={id_}"
        logger.debug(query)
        session = sessions[settings.get_actual_slave_index()]
        logger.debug(str(session.bind.url))
        item = await session.execute(text(query))
        if not (item := item.first()):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail_by_not_fount
            )
        return item

    @staticmethod
    async def get_all(
        sessions: List[AsyncSession],
        model: str,
        detail_by_not_fount: str = "Not found.",
        field_sort: str = "id",
        pagination: BasePaginationParams = None,
    ) -> list[object]:
        query: str = f"SELECT * FROM {model} ORDER BY {field_sort}"
        if pagination:
            query = pagination.add_pagination(query=query)
        logger.debug(query)
        session = sessions[settings.get_actual_slave_index()]
        logger.debug(str(session.bind.url))
        items = await session.execute(text(query))
        items = items.all()
        return items if len(items) > 1 else []

    @staticmethod
    async def search(
        sessions: List[AsyncSession],
        model: str,
        data: dict,
        detail_by_not_fount: str = "Not found.",
        pagination: BasePaginationParams = None,
    ) -> list[object]:
        data = {k: v for k, v in data.items() if v}
        query = query = f"SELECT * FROM {model} WHERE " + " AND ".join(
            f"{key} like '{str(value).lower()}%'" for key, value in data.items()
        )
        if pagination:
            query = pagination.add_pagination(query=query)
        logger.debug(query)
        session = sessions[settings.get_actual_slave_index()]
        logger.debug(str(session.bind.url))
        items = await session.execute(text(query))
        items = items.all()
        return items
