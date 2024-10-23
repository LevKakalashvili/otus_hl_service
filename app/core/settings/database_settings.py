import time

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Настройки базы данных"""

    DB_URI_MASTER: str = Field(
        default="postgresql+asyncpg://admin:admin@0.0.0.0:5432/social_network_db",
        description="Строка подключения к master бд",
    )
    DB_URI_SLAVE_1: str = Field(
        default="postgresql+asyncpg://admin:admin@0.0.0.0:5432/social_network_db",
        description="Строка подключения к slave_1 бд",
    )
    DB_URI_SLAVE_2: str = Field(
        default="postgresql+asyncpg://admin:admin@0.0.0.0:5432/social_network_db",
        description="Строка подключения к slave_2 бд",
    )
    DB_MASTER_INDEX: int = Field(default=0)
    DB_SLAVE_1_INDEX: int = Field(default=1)
    DB_SLAVE_2_INDEX: int = Field(default=2)

    def get_actual_slave_index(self) -> int:
        current_second = time.localtime().tm_sec
        return (
            self.DB_SLAVE_1_INDEX if current_second % 2 == 0 else self.DB_SLAVE_2_INDEX
        )
