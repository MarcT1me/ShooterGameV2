from abc import ABC
from typing_extensions import deprecated, Callable, Self

import Engine


@deprecated("use only in engine")
class Defer(ABC):
    def __init__(self,
                 name: str,
                 callback: Callable,
                 *,
                 attach_clock: 'Engine.time.Clock' = None,
                 disposable: bool = True):
        self._attach_clock: 'Engine.time.Clock' = attach_clock

        self.name: str = name

        self._callback: Callable = callback
        self._disposable: bool = disposable

        self.check: Callable[[Self], bool] = None

    def __str__(self) -> str:
        return f"Defer<{self.__class__.__name__}>(name={self.name}, disposable={self._disposable})"

    def attach_to_clock(self, attach_clock: 'Engine.time.Clock'):
        self._attach_clock = attach_clock

    def handle(self):
        if self.check(self):
            if self._callback: self._callback()
            if self._disposable:
                self.stop()

    def start(self):
        self._attach_clock.data.defers[self.name] = self

    def stop(self):
        self._attach_clock.data.defers.pop(self.name)
