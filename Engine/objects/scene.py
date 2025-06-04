from abc import ABC

import pygame

import Engine
from Engine.objects.object import Object


class Scene(ABC, Object):
    data: 'Engine.objects.SceneData'

    def __init__(self, data: 'Engine.objects.SceneData'):
        super().__init__(data)

        self.camera = Engine.objects.Camera(data.camera_data)

    def add_object(self, _object: Object) -> None:
        self.data.objects[_object.data.name] = _object

    def pop_object(self, name: str) -> Object:
        return self.data.objects.pop(name)

    def get_object(self, name: str) -> Object:
        return self.data.objects[name]

    def reload_data(self, data: 'Engine.objects.ObjectData'):
        for obj in self.data.objects.values():
            obj.reload_data(data)

    def event(self, event: pygame.event.Event) -> None:
        for obj in set(self.data.objects.values()):
            obj.event(event)

    def update(self, delta_time: float) -> None:
        for obj in set(self.data.objects.values()):
            obj.update(delta_time)

    def render(self) -> None:
        for obj in self.data.objects.values():
            obj.render()
