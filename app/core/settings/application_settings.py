from pydantic import Field
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """Настройки приложения"""

    ENVIRONMENT: str = Field(default="dev")
    SERVICE: str = Field(default="social_network_backend")

    LOGGING_LEVEL: str = Field(default="DUBUG")

    SERVER_HOST: str = Field(default="0.0.0.0")
    SERVER_PORT: int = Field(default="8000")
    SERVER_DEBUG: bool = Field(default=True)
    SERVER_RELOADED: bool = Field(default=False)
    SERVER_WORKERS: int = Field(default=1)

    ORIGINS: str = Field(default="*")

    PROJECT_VERSION: str = Field(default="0.1.0")
    PROJECT_DESCRIPTION: str = Field(
        default="Сервис социальной сети для учебного проекта"
    )

    SENTRY_DSN: str = Field(default="")
