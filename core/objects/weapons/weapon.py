from abc import ABC
from typing import Optional
from dataclasses import dataclass

import pygame
import glm

import Engine

import core


@dataclass
class WeaponData(Engine.objects.game_object.GameObjectData):
    weapon_type: str

    player_data: Optional['core.objects.PlayerData'] = None

    is_active: bool = False
    is_shooting: bool = False


class Weapon(ABC, Engine.objects.game_object.GameObject):
    data: WeaponData

    # weapon
    HAND_OFFSET = glm.vec2(0)

    # bullet data
    BULLET_SPEED: int = 1
    DAMAGE: int = 25

    def __init__(self, data: WeaponData):
        super().__init__(data)

        self.img: Optional[pygame.Surface] = self._get_asset("image", self.data.weapon_type)

        self.bullet_iter = 0

    @property
    def player_data(self) -> 'Optional[core.objects.PlayerData]':
        return self.data.player_data

    @player_data.setter
    def player_data(self, player_name: Optional[str]):
        if player_name is None:
            self.data.player_data = None
            return
        self.data.player_data = self.app.scene.data.objects[player_name].data

    def event(self, event: pygame.event.Event) -> None:
        if not self.data.is_active: return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.data.is_shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.data.is_shooting = False

    def update(self, _: float) -> None:
        if self.player_data is not None:
            self.data.transform.position = (
                    self.player_data.transform.position +
                    self._get_hand_offset(self.player_data)
            )
            self.data.transform.set_direction(self.player_data.transform.direction)

    def render(self) -> None:
        rotated_img, rect = self._rotate_img(self.img)
        self.app.window.surface.blit(rotated_img, rect.topleft)

    def _fire(self, position: glm.vec2, direction: glm.vec2, player_data: 'core.objects.PlayerData'):
        bullet = core.objects.Bullet(
            core.objects.BulletData(
                name=f"{self.cls_name}_{self.data.name}_bullet_index_{self.bullet_iter}",

                transform=Engine.objects.game_object.Transform(
                    position=position + self._get_hand_offset(player_data),  # player_data.transform.position.xy
                    direction=direction,  # player_data.transform.direction.xy
                ),
                speed=self.__class__.BULLET_SPEED,
                damage=self.__class__.DAMAGE,

                player_name=player_data.name
            )
        )
        self.app.scene.add_object(bullet)
        self.bullet_iter += 1

    def _get_hand_offset(self, player_data: 'core.objects.PlayerData') -> glm.vec2:
        angle = player_data.transform.get_angle_rad()

        base_offset = self.__class__.HAND_OFFSET.xy

        return glm.vec2(
            base_offset.x * glm.cos(angle) - base_offset.y * glm.sin(angle),
            base_offset.x * glm.sin(angle) + base_offset.y * glm.cos(angle)
        )

    def is_in_pickup_range(self, player_pos: glm.vec2, radius: float) -> bool:
        distance = glm.distance(player_pos, self.data.transform.position)
        return distance <= radius

    def pickup(self, player_data: 'core.objects.PlayerData'):
        self.player_data = player_data.name
        self.data.is_active = True
        player_data.current_weapon_name = self.data.name

    def drop(self):
        self.player_data = None
        self.data.is_active = False
        self.data.is_shooting = False
