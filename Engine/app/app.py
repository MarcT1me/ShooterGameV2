from typing import Self, final
from abc import ABC, abstractmethod

import pygame
from loguru import logger
import glm

import Engine.window

from Engine.error.IErrorHandler import IErrorHandler


class App(ABC, Engine.objects.Object, IErrorHandler):
    data: 'Engine.app.AppData'
    error_category = Engine.error.ErrorCategory.Engine | Engine.error.ErrorCategory.App

    reg_asset_types: list[Engine.assets.AssetType] = [
        Engine.assets.AssetType(
            type_name="image",
            asset_loader=Engine.assets.default.ImageAssetLoader()
        ),
        Engine.assets.AssetType(
            type_name="sound",
            asset_loader=Engine.assets.default.SoundAssetLoader()
        )
    ]

    _instance: Self = None

    @abstractmethod
    def prepare_instance(self) -> 'Engine.app.AppData':
        ...

    def __init__(self):
        App._instance = self
        self.running: bool = True

        self.window: Engine.window.Window = None
        self.clock: Engine.time.Clock = None

        self.event_list: list[pygame.event.EventType] = []

        self.key_list: pygame.key.ScancodeWrapper = []

        self.mouse_pos: glm.vec2 = glm.vec2(0)
        self.mouse_rel: glm.vec2 = glm.vec2(0)
        self.mouse_btn: glm.bvec3 = glm.bvec3()

        self.errors: list[Engine.error.Error] = []

        self.asset_manager = Engine.assets.AssetManager(App.reg_asset_types)

        app_data = self.prepare_instance()
        super().__init__(app_data)
        self.__init_sub_systems()

        logger.success("App - init")

    @staticmethod
    @final
    def get() -> 'App':
        return App._instance

    def __init_sub_systems(self) -> None:
        pygame.init()

        self.window = Engine.window.Window(
            self.data.win_data,
            caption=self.data.name
        )

        self.clock = Engine.time.Clock(self.data.clock_data)

        logger.success("App - sub-systems init")

    def reload_data(self, data: 'Engine.objects.ObjectData'):
        if self.scene is not None:
            self.scene.reload_data(data)

    @final
    def run(self, cth: Engine.error.Catch) -> None:
        while self.running:
            cth.try_func(
                self.__events,
                error_category=cth.error_category | Engine.error.ErrorCategory.Event,
                error_level=Engine.error.ErrorLevel.First
            )

            # check running after events
            if not self.running: break

            cth.try_func(
                self.__updating,
                error_category=cth.error_category | Engine.error.ErrorCategory.Update,
                error_level=Engine.error.ErrorLevel.Second
            )

            cth.try_func(
                self.__rendering,
                error_category=cth.error_category | Engine.error.ErrorCategory.Render,
                error_level=Engine.error.ErrorLevel.Second
            )

            self.clock.tick()

    def __events(self):
        self.event_list = pygame.event.get()
        self.key_list = pygame.key.get_pressed()

        self.mouse_pos = glm.vec2(pygame.mouse.get_pos())
        self.mouse_rel = glm.vec2(pygame.mouse.get_rel())

        self.mouse_btn = glm.bvec3(pygame.mouse.get_pressed())
        # handle events
        for event in self.event_list:
            self.__default_event(event)
            self.event(event)

    def __default_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.quit()
        self.window.event(event)

    def __updating(self):
        # update
        self.update(self.clock.data.delta_time)

    def __rendering(self):
        # render
        self.window.clear()
        self.render()
        self.window.render()

    @final
    def start(self):
        with Engine.error.Catch(
                name="ENGINE_App_Starty_Catch",
                error_category=App.error_category,
                error_level=Engine.error.ErrorLevel.Second
        ) as cth:
            self.run(cth)
            self.on_exit()

    @final
    def quit(self) -> None:
        self.running = False

    @final
    def critical_error(self, error: Engine.error.Error) -> bool:
        self.errors.append(error)
        if error.level is Engine.error.ErrorLevel.Second:
            self.quit()
        return not isinstance(error.exc, KeyboardInterrupt)

    def on_error(self, error: Engine.error.Error) -> bool:
        logger.exception(
            f"App got error:\n"
            f"\texc: {error.exc}"
            f"\ttime_stamp: {error.time_stamp}"
            f"\tlevel: {error.level.name}"
            f"\tcategory: {error.category.name}"
        )
        if error.level is not Engine.error.ErrorLevel.NotCritical:
            return self.critical_error(error)
