from dataclasses import dataclass, field
from typing import Optional, Self

import Engine
from glm import vec2, ivec4


@dataclass
class WinData:
    size: vec2
    vsync: Optional[bool] = field(default=False)
    display: Optional[int] = field(default=0)
    flags: Optional[int] = field(default=0)
    full_mode: 'Optional[Engine.window.FullMode]' = None

    clear_color: ivec4 = field(default=ivec4(0, 0, 0, 255))
    icon_path: str = "assets\\icon.png"


    def __post_init__(self):
        self.size = vec2(self.size)
        self.clear_color = ivec4(self.clear_color)

    def get_kwargs(self) -> dict:
        kwargs = {
            "size": self.size,
            "flags": self.flags,
        }
        if self.vsync: kwargs["vsync"] = True
        if self.display is not None: kwargs["display"] = self.display

        return kwargs

    def check_difference(self, new_win_data: Self) -> bool:
        return self.get_kwargs() != new_win_data.get_kwargs()
