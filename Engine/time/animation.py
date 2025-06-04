from typing import Callable, Any, Self
from dataclasses import dataclass

from Engine.objects.object_data import ObjectData
from Engine.time.defer.time_defer import TimeDefer


@dataclass
class AnimationData(ObjectData):
    frames: dict[float, Any]
    time_offset: float = 0.0
    frame_handle_func: Callable[['Animation'], Any] = None


class Animation(TimeDefer):
    def __init__(self, data: AnimationData):
        super().__init__(
            data.name, None,
            disposable=True,
            time_offset=data.time_offset
        )
        self.animation_start_time: float = None
        self._frame_handle_func: Callable[[Self], Any] = data.frame_handle_func
        self.check = self._check

        self.frames: dict[float, Any] = data.frames
        self._sorted_times = tuple(sorted(self.frames.keys()))
        self._end_frame: int = len(self._sorted_times) - 1

        self.current_frame_index = -1
        self.animation_value: Any = None
        self.current_frame: dict[float, Any] = {0, self.animation_value}

        self.next_frame: dict[float, Any] = self.get_next_frame()

    def handle(self):
        self._update_animation()
        super().handle()

    def get_time_passed_from_start(self):
        return self._attach_clock.get_time() - self.animation_start_time

    def get_time_passed_from_last_frame(self):
        return self._attach_clock.get_time() - self.start_time

    def get_next_frame(self) -> tuple[float, Any]:
        return self._sorted_times[self.current_frame_index], self.frames[self.time_offset]

    def _update_animation(self):
        self.animation_value = self._frame_handle_func(self)

    def _restart(self):
        if self.current_frame_index >= self._end_frame:
            self.stop()
            return

        super()._restart()
        self.current_frame_index += 1
        self.animation_value = self.frames[self.time_offset]
        self.current_frame = {self._sorted_times[self.current_frame_index]: self.animation_value}

    def start_animation(self):
        self.animation_start_time = self._attach_clock.get_time()
        self.current_frame_index = -1
        self.start()

    def stop_animation(self):
        super().stop()

    def _check_and_stop(self):
        if self.current_frame_index >= self._end_frame:
            super().stop()

    def stop(self):
        if self.current_frame_index >= self._end_frame:
            super().stop()
        else:
            self._restart()
