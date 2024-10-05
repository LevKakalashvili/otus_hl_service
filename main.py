import uvicorn
from loguru import logger
from app.core.monitoring import logger as monitoring_logger

from app.core.settings import settings

# start service
if __name__ == "__main__":
    monitoring_logger
    logger.info(f"{settings.SERVICE.capitalize()} started")
    uvicorn.run(
        "app.server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_RELOADED,
        workers=settings.SERVER_WORKERS,
    )
