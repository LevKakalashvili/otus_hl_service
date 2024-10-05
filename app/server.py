from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import health_check_router, user_router
from app.core.settings import Settings, settings
from app.handlers import exception_handler


class Server:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.app = self.create_server()

    def _add_middleware(self):
        """Добавление мидлвейр"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in self._settings.ORIGINS.split(";")],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "HEAD", "OPTIONS", "DELETE"],
            allow_headers=["*"],
        )

    def _add_exception_handlers(self):
        """Добавление обработчиков исключений"""
        self.app.add_exception_handler(Exception, exception_handler)

    def _add_routes(self):
        """Добавление роутов эндпоинтов"""
        self.app.include_router(health_check_router)
        self.app.include_router(user_router)

    def create_server(self) -> FastAPI:
        """Создание экземпляра сервера"""
        return FastAPI(
            title=self._settings.SERVICE,
            debug=self._settings.SERVER_DEBUG,
            version=self._settings.PROJECT_VERSION,
            description=self._settings.PROJECT_DESCRIPTION,
            docs_url=(
                "/api/docs" if self._settings.ENVIRONMENT in ("dev", "local") else None
            ),
            redoc_url=(
                "/api/redoc" if self._settings.ENVIRONMENT in ("dev", "local") else None
            ),
            openapi_url="/api/openapi.json",
        )

    def get_app(self) -> FastAPI:
        """Получение экземпляра приложения"""
        self._add_routes()
        self._add_middleware()
        self._add_exception_handlers()
        return self.app


# create app
app = Server(settings).get_app()
