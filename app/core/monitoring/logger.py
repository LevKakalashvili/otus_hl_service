from loguru import logger

from app.core.settings.general_settings import settings

logger.add(
    settings.LOG_FILE,
    rotation="50 MB",
    retention=5,
)