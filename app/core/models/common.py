from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import Select


class BasePaginationParams(BaseModel):
    """
    Стандартная модель данных параметров для GET запросов с пагинацией
    """

    limit: int | None = Field(
        Query(100, ge=1, le=100, description="Размер ограничения")
    )
    offset: int | None = Field(Query(0, ge=0, description="Размер смещения"))

    def add_pagination(self, query: Union[str, Select]) -> Union[str, Select]:
        """
        Добавить пагинацию (ограничение/смещение) к запросу
        """
        if isinstance(query, str):
            return f"{query} LIMIT {self.limit} OFFSET {self.offset}"

        return query.offset(self.offset).limit(self.limit)
