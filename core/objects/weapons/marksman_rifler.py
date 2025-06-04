from dataclasses import dataclass

import glm

from core.objects.weapons.weapon import WeaponData
from core.objects.weapons.weaon_type import SemiAutomat


@dataclass
class MarksmanRifleData(WeaponData):
    weapon_type: str = "scar_l"


class MarksmanRifle(SemiAutomat):
    data: MarksmanRifleData

    BULLET_SPEED = 15
    FIRE_OFFSET = 0.125
    DAMAGE = 55

    HAND_OFFSET = glm.vec2(24, 6)
