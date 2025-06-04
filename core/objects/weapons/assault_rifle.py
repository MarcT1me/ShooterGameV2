from dataclasses import dataclass

import glm

from core.objects.weapons.weapon import WeaponData
from core.objects.weapons.weaon_type import Automat


@dataclass
class AssaultRifleData(WeaponData):
    weapon_type: str = "assault_rifle"


class AssaultRifle(Automat):
    data: AssaultRifleData

    BULLET_SPEED = 10
    FIRE_RATE = 400
    DAMAGE = 30

    HAND_OFFSET = glm.vec2(21, 5)
