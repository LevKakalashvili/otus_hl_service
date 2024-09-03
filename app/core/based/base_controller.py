from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class BaseController:
    """
    Базовый контроллер
    """

    @staticmethod
    async def create(
        session: AsyncSession,
        model: str,
        data: dict,
    ) -> int:
        if isinstance(data, dict) and data:
            query = (
                f"INSERT INTO {model} "
                f"({", ".join([f'"{key}"' for key in data.keys()])}) "
                f"VALUES "
                f"({", ".join([f"'{value}'"for value in data.values()])}) "
                f"RETURNING id"
            )
            item = await session.execute(text(query))
        return list(item)[0][0]

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        model: str,
        id_: int,
        detail_by_not_fount: str = "Not found.",
    ) -> object:
        item = await session.execute(text(f"SELECT * FROM {model} WHERE id={id_}"))
        if not (item := item.first()):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail_by_not_fount
            )
        return item

    @staticmethod
    async def get_all(
        session: AsyncSession, model: str, detail_by_not_fount: str = "Not found."
    ) -> list[object]:
        items = await session.execute(text(f"SELECT * FROM {model}"))
        items = items.all()
        return items if len(items) > 1 else []
