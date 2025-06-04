from dataclasses import dataclass, field
from typing import Optional

import Engine


@dataclass
class ClockData:
    tps: int
    delta_time: float = field(init=False, default=0)

    speed_roster: Optional[dict] = field(default_factory=dict)
    timers: dict[str, 'Engine.time.Timer'] = field(init=False, default_factory=dict)
    defers: dict[str, 'Engine.time.defer.Defer'] = field(init=False, default_factory=dict)
