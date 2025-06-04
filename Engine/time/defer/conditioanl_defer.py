from typing import Callable

from Engine.time.defer.defer import Defer


class ConditionalDefer(Defer):
    def __init__(self,
                 *args,
                 conditional_lambda: Callable[[Defer], bool],
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.check = conditional_lambda
