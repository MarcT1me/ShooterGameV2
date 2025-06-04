from typing import TYPE_CHECKING
from abc import ABCMeta, abstractmethod

import pygame

import Engine

from Engine.error.IErrorCategory import IErrorCategory


class Object(IErrorCategory, metaclass=ABCMeta):
    data: 'Engine.objects.ObjectData'
    error_category: 'Engine.error.ErrorCategory' = Engine.error.ErrorCategory.Object

    def __init__(self, data: 'Engine.objects.ObjectData'):
        self.app = Engine.App.get()
        self.data = data

    def reload_data(self, data: 'Engine.objects.ObjectData'):
        ...

    def on_exit(self):
        ...

    @property
    def cls_name(self) -> str:
        return self.__class__.__name__

    if TYPE_CHECKING:
        @abstractmethod
        def event(self, event: pygame.event.Event) -> None:
            ...

        @abstractmethod
        def update(self, delta_time: float) -> None:
            ...

        @abstractmethod
        def render(self) -> None:
            ...
