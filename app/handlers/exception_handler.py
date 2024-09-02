import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger()


async def exception_handler(request: Request, exc: Exception):
    logger.exception(exc, extra={"uuid": request.state.trace_id, "type": "app-error"})
    return JSONResponse(
        status_code=500,
        content={
            "uuid": request.state.trace_id,
            "status": "error",
            "message": "Произошла внутренняя ошибка",
        },
    )
