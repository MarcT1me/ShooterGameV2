from typing import Optional

import pygame

from Engine.objects.game_object.game_object import GameObjectData, GameObject


class Camera(GameObject):
    def __init__(self, data: GameObjectData):
        super().__init__(data)
        self.attach_object: Optional[GameObject] = None

    def attach_to_object(self, obj: GameObject):
        self.attach_object = obj

    def event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, delta_time: float) -> None:
        if self.attach_object is not None:
            self.data.pos = self.attach_object.data.transform.position

    def render(self) -> None:
        pass
