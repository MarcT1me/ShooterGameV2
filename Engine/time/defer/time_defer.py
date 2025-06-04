from Engine.time.defer.defer import Defer


class TimeDefer(Defer):
    def __init__(self,
                 *args,
                 time_offset: float,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time: float = 0
        self.time_offset = time_offset
        self.check = self.__check

    def __check(self, *args, **kwargs):
        is_passed: bool = self._check()
        if is_passed:
            self._restart()
        return is_passed

    def _check(self, *args, **kwargs) -> bool:
        cur_time: float = self._attach_clock.get_time()
        return cur_time - self.start_time > self.time_offset

    def _restart(self):
        self.start_time = self._attach_clock.get_time()

    def start(self) -> None:
        self.start_time = self._attach_clock.get_time()
        super().start()
