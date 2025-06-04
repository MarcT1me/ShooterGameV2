from typing import Optional

from dataclasses import dataclass

import pygame
import glm

import Engine

import core
from Engine.objects.game_object import GameObjectData, GameObject


@dataclass
class PlayerData(GameObjectData):
    speed: float
    velocity: glm.vec2 = glm.vec2(0)

    current_weapon_name: Optional[str] = None


class _NearistWeaponTitleAnimation(Engine.time.Animation):
    def __init__(self):
        app = Engine.App.get()

        data: Engine.time.AnimationData = Engine.time.AnimationData(
            name=f"{self.__class__.__name__}_{Engine.get_identifier()}",
            frames={
                0.0: 0,
                0.125: app.window.data.size.y / 4,
                0.25: 0,
            }
        )
        super().__init__(data)

    def _update_animation(self):
        print(self.current_frame_index, self.get_time_passed_from_last_frame(), self.animation_value)


class Player(GameObject):
    data: PlayerData

    MAX_VEL = 1
    MOVE_RESISTANCE_FACTOR = 0.8

    PICKUP_RADIUS = 80

    def __init__(self, data: PlayerData):
        super().__init__(data)

        self.img: Optional[pygame.Surface] = self._get_asset("image", "player")

        self.nearest_weapon: Optional[core.objects.weapons.Weapon] = None

    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self._pickup_weapon(self.nearest_weapon)
            elif event.key == pygame.K_q:
                self._drop_weapon()
            elif event.key == pygame.K_b:
                anim = _NearistWeaponTitleAnimation()
                self.app.clock.add_defer(anim, "defer")
                anim.start_animation()

    def _pickup_weapon(self, weapon: 'core.objects.weapons.Weapon') -> None:
        if self.nearest_weapon is None:
            return
        weapon.pickup(self.data)
        print("pickup ", weapon.data.name)

    def _drop_weapon(self) -> None:
        if self.data.current_weapon_name is None:
            return
        cur_weapon: core.objects.weapons.Weapon = self.app.scene.data.objects[self.data.current_weapon_name]
        cur_weapon.drop()
        print("drop ", cur_weapon.data.name)

    def update(self, delta_time: float) -> None:
        self._calc_angle()
        self._calc_vel(self.data.speed)
        self._calc_pos(delta_time)
        self._update_nearest_weapon()

    def _calc_angle(self) -> None:
        # calculate angle
        self.data.transform.direction = glm.normalize(
            self.app.mouse_pos - self.data.transform.position - self.app.scene.camera.data.transform.position
        )

    def _calc_vel(self, speed: float) -> None:
        # calculate movement
        if self.app.key_list[pygame.K_w]:
            self.data.velocity.y -= speed
        if self.app.key_list[pygame.K_s]:
            self.data.velocity.y += speed
        if self.app.key_list[pygame.K_a]:
            self.data.velocity.x -= speed
        if self.app.key_list[pygame.K_d]:
            self.data.velocity.x += speed

        self.data.velocity *= Player.MOVE_RESISTANCE_FACTOR

        if glm.length(self.data.velocity) < 0.05:
            self.data.velocity = glm.vec2(0)
        elif glm.length(self.data.velocity) > Player.MAX_VEL:
            self.data.velocity = glm.normalize(self.data.velocity)

    def _calc_pos(self, delta_time: float) -> None:
        self.data.transform.move_to(self.data.velocity * delta_time)

    def _update_nearest_weapon(self) -> None:
        self.nearest_weapon = None
        min_dist = self.__class__.PICKUP_RADIUS + 1

        for obj in self.app.scene.data.objects.values():
            if isinstance(obj, core.objects.weapons.Weapon) and not obj.data.is_active:
                distance = glm.length(
                    self.data.transform.position - obj.data.transform.position
                )
                if distance < self.__class__.PICKUP_RADIUS and distance < min_dist:
                    min_dist = distance
                    self.nearest_weapon = obj

    def render(self) -> None:
        # blit img
        rotated_img, rect = self._rotate_img(self.img)

        if rotated_img is None: return  # validate render data

        pygame.draw.circle(self.app.window.surface, "green", rect.center, self.img.get_width() / 2)
        self.app.window.surface.blit(rotated_img, rect.topleft)
