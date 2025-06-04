from enum import Flag, auto


class ErrorCategory(Flag):
    Unknown = auto()
    Engine = auto()

    Object = auto()
    App = auto()
    SubSystem = auto()

    Event = auto()
    Update = auto()
    Render = auto()

    @classmethod
    def get_category_from_handler(cls, general, reserve_handler):
        if general is not None:
            return general
        elif reserve_handler is not None:
            return reserve_handler.error_category
        else:
            return cls.Unknown
