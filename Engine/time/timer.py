from Engine.time.defer.time_defer import TimeDefer


class Timer(TimeDefer):
    def __init__(self,
                 name: str,
                 time_offset: float):
        super().__init__(
            name, None,
            disposable=False,
            time_offset=time_offset
        )
