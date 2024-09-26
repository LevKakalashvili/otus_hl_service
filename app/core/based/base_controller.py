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
        # INSERT INTO public."user"
        # ("name", sur_name, birth_date, sex, city, interest, id)
        # VALUES('Иван', 'Иванов', '2000-01-01', NULL, 'Sarov', 'cats, pets, football', 1);
        if isinstance(data, dict) and data:
            query = (
                f"INSERT INTO {model} ("
                + ", ".join(['"' + key_ + '"' for key_ in data.keys()])
                + ") VALUES ("
                + ", ".join("'" + str(value) + "'" for value in data.values())
                + ") RETURNING id"
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

    @staticmethod
    async def search(
        session: AsyncSession,
        model: str,
        data: dict,
        detail_by_not_fount: str = "Not found.",
    ) -> list[object]:
        query = query = f"SELECT * FROM {model} WHERE " + " AND ".join(
            f"{key} ilike '{str(value)}%'" for key, value in data.items()
        )
        items = await session.execute(text(query))
        items = items.all()
        return items if len(items) > 1 else []
