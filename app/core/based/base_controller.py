from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
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
                f"INSERT INTO {model} ("
                + ", ".join(['"' + key_ + '"' for key_ in data.keys()])
                + ") VALUES ("
                + ", ".join("'" + str(value) + "'" for value in data.values())
                + ") RETURNING id"
            )
            try:
                item = await session.execute(text(query))
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=e.args[0],
                )
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
        session: AsyncSession, model: str, detail_by_not_fount: str = "Not found.", field_sort: str = "id"
    ) -> list[object]:
        items = await session.execute(text(f"SELECT * FROM {model} ORDER BY {field_sort} DESC"))
        items = items.all()
        return items if len(items) > 1 else []

    @staticmethod
    async def search(
        session: AsyncSession,
        model: str,
        data: dict,
        detail_by_not_fount: str = "Not found.",
    ) -> list[object]:
        data = {k: v for k, v in data.items() if v}
        query = query = f"SELECT * FROM {model} WHERE " + " AND ".join(
            f"{key} ilike '{str(value)}%'" for key, value in data.items()
        )
        items = await session.execute(text(query))
        items = items.all()
        # items
        # return items if len(items) > 1 else []
        return items
