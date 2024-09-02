import enum


class IntEnum(enum.IntEnum):
    def __str__(self):
        return str(self.value)

    def translate(self, *_):
        return self.value

    @classmethod
    def get_values_list(cls):
        return list(cls)  # type: ignore


class StrEnum(str, enum.Enum):
    def __str__(self):
        return str(self.value)

    def translate(self, *_):
        return self.value

    @classmethod
    def get_values_list(cls):
        return list(cls)  # type: ignore
