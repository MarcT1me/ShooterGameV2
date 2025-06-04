from typing import Self, Callable

import Engine
from Engine.error.IErrorHandler import IErrorHandler

from loguru import logger


class Catch:
    roster: dict[str, Self] = {}

    def __init__(self, name: str, *, handler: IErrorHandler = None,
                 error_category: 'Engine.error.ErrorCategory' = None,
                 error_level: 'Engine.error.ErrorLevel' = None):
        self.name: str = name

        if name in Catch.roster:
            raise Exception(f"Catch with name {name} already in roster")

        self.handler: IErrorHandler = handler

        self.error_category: Engine.error.ErrorCategory = self.get_err_category(error_category, handler)
        self.error_level: Engine.error.ErrorLevel = self.get_err_level(error_level, handler)

    @staticmethod
    def get_err_category(error_category, handler):
        return Engine.error.ErrorCategory.get_category_from_handler(
            error_category, handler
        )

    @staticmethod
    def get_err_level(error_level, handler):
        return Engine.error.ErrorLevel.get_level_from_handler(
            error_level, handler
        )

    def __enter__(self) -> Self:
        Catch.roster[self.name] = self
        return self

    def try_func[T](
            self,
            func: Callable[[...], T],
            *args,
            error_category: 'Engine.error.ErrorCategory' = None,
            error_level: 'Engine.error.ErrorLevel' = None,
            **kwargs
    ) -> T:
        app_instance: Engine.App = Engine.App.get()
        try:
            return func(*args, **kwargs)
        except Engine.error.Error as err:
            self._handle_err(err)
            return err
        except Exception as e:
            err: Engine.error.Error = Engine.error.Error(
                e, app_instance.clock.get_time(),
                self.get_err_category(error_category, self.handler),
                self.get_err_level(error_level, self.handler)
            )
            
            self._handle_err(err)
            return err

    def __exit__(self, exc_type: type, exc_val: 'Engine.error.Error | Exception', _) -> bool:
        if exc_type is not None:
            self._context_got_error(exc_type, exc_val)
        Catch.roster.pop(self.name)
        return bool(exc_type)

    def _context_got_error(self, exc_type: type, exc_val: 'Exception | Engine.error.Error'):
        # Проверяем, является ли исключение экземпляром класса Exception или его подкласса
        logger.warning(
            f"Catch {self.name} got a error:\n"
            f"type: {exc_type}\n"
            f"exc: {exc_val}\n"
            f"level: {self.error_level}"
        )
        if issubclass(exc_type, Engine.error.Error):
            self._handle_err(exc_val)
        else:
            err: Engine.error.Error = Engine.error.Error(
                exc=exc_val,
                time_stamp=Engine.App.get().clock.get_time(),
                category=self.error_category,
                level=self.error_level
            )
            self._handle_err(err)

    def _handle_err(self, err: 'Engine.error.ErrorLevel'):
        handler = self.handler if self.handler else Engine.App.get()
        handler.on_error(err)
