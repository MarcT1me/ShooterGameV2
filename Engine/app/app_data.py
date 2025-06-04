from dataclasses import dataclass

import Engine


@dataclass
class AppData(Engine.objects.ObjectData):
    win_data: Engine.window.WinData
    clock_data: Engine.time.ClockData
