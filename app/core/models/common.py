from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import Select


class BasePaginationParams(BaseModel):
    """
    Стандартная модель данных параметров для GET запросов с пагинацией
    """

    limit: int | None = Field(
        Query(None, ge=1, le=100, description="Размер ограничения", example=100),
    )
    offset: int | None = Field(
        Query(None, ge=0, description="Размер смещения", example=0)
    )

    def add_pagination(self, query: Union[str, Select]) -> Union[str, Select]:
        """
        Добавить пагинацию (ограничение/смещение) к запросу
        """
        if isinstance(query, str):
            if self.limit is not None and self.offset is not None:
                return f"{query} LIMIT {self.limit} OFFSET {self.offset}"
            elif self.limit is not None and self.offset is None:
                return f"{query} LIMIT {self.limit} OFFSET 0"
            elif self.limit is None:
                return query

        return query.offset(self.offset).limit(self.limit)
