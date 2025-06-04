import time
from typing import Any, Optional

import Engine.time

import pygame
from loguru import logger


class Clock(Engine.objects.Object):
    data: 'Engine.time.ClockData'
    error_category = Engine.error.ErrorCategory.Engine | Engine.error.ErrorCategory.SubSystem

    def __init__(self, clock_data: 'Engine.time.ClockData'):
        super().__init__(clock_data)

        self._pg_clock = pygame.time.Clock()

        logger.success(
            "Clock init\n"
            f"data: {clock_data}"
        )

    def get_tps(self) -> float:
        """Get current FPS count"""
        return self._pg_clock.get_fps()

    @staticmethod
    def wait(ms: int) -> None:
        """Wait specified milliseconds"""
        pygame.time.wait(ms)

    @staticmethod
    def get_ticks() -> int:
        """Get milliseconds since program start"""
        return pygame.time.get_ticks()

    @staticmethod
    def get_time() -> float:
        return time.time()

    def timer(self, name) -> bool:
        return self.data.timers[name].check()

    def tick(self) -> None:
        for defer in tuple(self.data.defers.values()):
            defer.handle()

        self.data.delta_time = self._pg_clock.tick(self.data.tps)

    def __getitem__(self, path: str) -> Optional[Any]:
        category, name = path.split('/')

        match category:
            case "speed":
                return self.data.speed_roster[name]
            case "timer":
                return self.data.timers[name]
            case "defer":
                return self.data.defers[name]

    def add_defer(self, defer: 'Engine.time.defer.Defer', category: str) -> None:
        match category:
            case "timer":
                self.data.timers[defer.name] = defer
                defer.attach_to_clock(self)
                logger.success(
                    "Clock add defer - timer\n"
                    f"defer: {defer}"
                )
                return
            case "defer":
                self.data.defers[defer.name] = defer
                defer.attach_to_clock(self)
                logger.success(
                    "Clock add defer - defer\n"
                    f"defer: {defer}"
                )
                return
        logger.error(
            "Clock add defer - not implement defer type"
        )

    def set_speed(self, name: str, value: float) -> None:
        self.data.speed_roster[name] = value
