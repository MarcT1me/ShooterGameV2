from enum import Enum, auto


class ErrorLevel(Enum):
    NotCritical = auto()
    First = auto()
    Second = auto()

    @classmethod
    def get_level_from_handler(cls, general, reserve_handler):
        if general is not None:
            return general
        elif reserve_handler is not None:
            return reserve_handler.error_level
        else:
            return cls.Second
