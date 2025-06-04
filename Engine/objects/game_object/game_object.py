from abc import ABCMeta
from typing import Optional, Any
from dataclasses import dataclass

import pygame
import glm

import Engine
from Engine.objects.object_data import ObjectData
from Engine.objects.object import Object

@dataclass
class GameObjectData(ObjectData):
    transform: 'Engine.objects.game_object.Transform'


class GameObject(Object, metaclass=ABCMeta):
    data: GameObjectData

    def _get_asset(self, asset_type: str, asset_name: str) -> Optional[Any]:
        return Engine.can_be_empty_content(
            self.app.asset_manager.storage.get(asset_type).get(asset_name)
        )

    def _rotate_img(
            self, img: pygame.Surface
    ) -> tuple[pygame.Surface, pygame.Rect, float] | tuple[None, None]:
        if img is None: return None, None

        # rotate image on angle
        angle: float = self.data.transform.get_angle_deg()
        rotated_img = pygame.transform.rotate(img, -angle)
        center = self.data.transform.position - self.app.scene.camera.data.transform.position

        if glm.length(center) > glm.length(self.app.window.data.size): return None, None

        rect = rotated_img.get_rect(center=img.get_rect(center=center).center)
        return rotated_img, rect
