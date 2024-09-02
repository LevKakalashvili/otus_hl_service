import uvicorn

from app.core.settings import settings

# start service
if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_RELOADED,
        workers=settings.SERVER_WORKERS,
    )
