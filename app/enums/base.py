from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def list(cls) -> list[str]:
        return list(cls.__members__.values())
