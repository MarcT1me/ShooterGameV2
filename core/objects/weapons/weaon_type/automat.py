import Engine

import core
from core.objects.weapons.weapon import WeaponData, Weapon


class Automat(Weapon):
    FIRE_RATE: int = 300

    def __init__(self, data: WeaponData):
        super().__init__(data)
        self.fire_rate_timer = Engine.time.Timer(
            f"{self.cls_name}_{self.data.name}_fire_rate_timer",
            60 / self.__class__.FIRE_RATE
        )
        self.fire_rate_timer.attach_to_clock(self.app.clock)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        if self.data.is_shooting:
            if self.fire_rate_timer.check():
                player_data: core.objects.PlayerData = self.player_data
                if player_data is not None:
                    self._fire(player_data.transform.position, player_data.transform.direction, player_data)
