from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def as_list(cls):
        return [getattr(cls, m).value for m in cls.__members__ if not m.startswith("_")]


class ResponseCode(int, BaseEnum):
    """Коды ответов сервиса. Кладется в ответ поле "code" """

    VALIDATION_ERROR = 100  # ошибки валидации входных схем
    OK = 0
    ERROR = 900
