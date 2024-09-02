import json
import logging
import uuid
from datetime import datetime, timezone
from json import JSONEncoder
from logging.config import dictConfig

from pythonjsonlogger import jsonlogger


# Пользовательский кодировщик JSON, который применяет стандартный формат ISO 8601,
class ModelJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class LogFilter(logging.Filter):
    def __init__(self, service=None, environment=None, instance=None):
        self.service = service
        self.environment = environment
        self.instance = instance

    def filter(self, record):
        record.service = self.service
        record.environment = self.environment
        record.instance = self.instance
        return True


class JsonLogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Добавляю поле метки времени по умолчанию: now
        if not log_record.get("timestamp"):
            now = datetime.now(timezone.utc).isoformat()
            log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        if not log_record.get("type"):
            log_record["type"] = "internal"


# Configure Logging
def configure_logging(
    level: str = "DEBUG",
    service: str = None,
    environment: str = None,
    instance: str = None,
):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "()": JsonLogFormatter,
                    "format": """%(timestamp)s %(level)s %(service)s
                    %(environment)s %(instance)s %(type)s %(message)s""",
                    "json_encoder": ModelJsonEncoder,
                }
            },
            "filters": {
                "default": {
                    "()": LogFilter,
                    "service": service,
                    "environment": environment,
                    "instance": instance,
                }
            },
            "handlers": {
                "default_handler": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "filters": ["default"],
                    "formatter": "default",
                }
            },
            "root": {"level": level, "handlers": ["default_handler"]},
        }
    )
