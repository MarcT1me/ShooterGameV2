from dataclasses import dataclass
from random import random

import glm

import core
from core.objects.weapons.weapon import WeaponData
from core.objects.weapons.weaon_type import SemiAutomat


@dataclass
class ShotGunData(WeaponData):
    weapon_type: str = "shotgun"


class ShotGun(SemiAutomat):
    data: ShotGunData

    BULLET_SPEED = 1

    FIRE_OFFSET = 0.25
    DAMAGE = 20

    HAND_OFFSET = glm.vec2(17.5, 9)

    def _fire(self, position: glm.vec2, _: glm.vec2, player_data: 'core.objects.PlayerData'):
        angle: float = player_data.transform.get_angle_rad()
        for i in range(-5, 5):
            rand: float = (i + random()) / 30
            rand_angle = angle + rand
            super()._fire(
                position,
                glm.normalize(
                    glm.vec2(
                        glm.cos(rand_angle),
                        glm.sin(rand_angle)
                    )
                ),
                player_data
            )
