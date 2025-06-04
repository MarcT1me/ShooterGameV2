from dataclasses import dataclass

import pygame
import glm

from Engine.objects.game_object import GameObjectData, GameObject


@dataclass
class BulletData(GameObjectData):
    speed: float
    damage: int

    player_name: str


BULLET_IMPACT_EVENT: int = pygame.event.custom_type()


class Bullet(GameObject):
    data: BulletData

    def __init__(self, data: BulletData):
        super().__init__(data)
        self.vel = self.data.transform.direction * self.data.speed
        self.last_pos: glm.vec2 = self.data.transform.position

    def event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.last_pos = self.data.transform.position.xy
        self.data.transform.move_to(self.vel * delta_time)

        if glm.length(self.data.transform.position) > glm.length(self.app.window.data.size):
            event = pygame.event.Event(
                BULLET_IMPACT_EVENT,
                name=self.data.name,
                impact_target=None
            )
            pygame.event.post(event)

    def render(self) -> None:
        if not self.app.data.is_release:
            pygame.draw.line(
                self.app.window.surface, "purple",
                self.last_pos - self.app.scene.camera.data.transform.position,
                self.data.transform.position - self.app.scene.camera.data.transform.position
            )
        pygame.draw.circle(
            self.app.window.surface, "red",
            self.data.transform.position - self.app.scene.camera.data.transform.position,
            2 if self.app.data.is_release else 10
        )
