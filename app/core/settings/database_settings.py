from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Настройки базы данных"""

    DB_URI: str = Field(
        default="postgresql+asyncpg://admin:admin@0.0.0.0:5432/social_network_db",
        description="Строка подключения к бд",
    )
