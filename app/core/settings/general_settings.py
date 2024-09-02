from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

from .application_settings import ApplicationSettings
from .database_settings import DatabaseSettings


class GeneralSettings(
    ApplicationSettings,
    DatabaseSettings,
):
    """Объединяющий класс настроек приложения"""

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> BaseSettings:
    return GeneralSettings()


Settings = Annotated[GeneralSettings, Depends(get_settings)]
settings = Settings()
