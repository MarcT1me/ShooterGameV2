from typing import TYPE_CHECKING

import Engine

import pygame
from glm import ivec2
from loguru import logger


class Window(Engine.objects.Object):
    data: 'Engine.window.WinData'
    error_category = Engine.error.ErrorCategory.Engine | Engine.error.ErrorCategory.SubSystem

    def __init__(self, win_data: 'Engine.window.WinData',
                 caption: str):
        super().__init__(win_data)

        self.caption = caption
        self.icon = pygame.image.load(win_data.icon_path)

        self.surface: pygame.Surface = None

        logger.debug("Window init")

        self.setup_window()

    def reload_data(self, data: 'Engine.window.WinData'):
        self.data = data
        self.setup_window()

        logger.success("Window reload data\n")

    def clear(self) -> None:
        self.surface.fill(self.data.clear_color)

    def setup_window(self) -> None:
        self._reinit_pg_sys()
        kwargs = self.data.get_kwargs()
        flags = self.data.flags

        if self.data.full_mode is Engine.window.FullMode.Frameless:
            desktop_sizes = pygame.display.get_desktop_sizes()
            self.data.size = desktop_sizes[self.data.display]
            kwargs["size"] = self.data.size
        elif self.data.full_mode is Engine.window.FullMode.Desktop:
            flags |= pygame.FULLSCREEN
        else:
            kwargs.pop("display")

        kwargs["flags"] = flags
        self._set_mode(**kwargs)
        self._set_window_frame()

        logger.success(
            "Window setup\n"
            f"data: {self.data}"
        )

    @staticmethod
    def _reinit_pg_sys():
        pygame.display.quit()
        pygame.display.init()

    if TYPE_CHECKING:
        def _set_mode(self,
                      *,
                      size: ivec2,
                      vsync: bool,
                      display: int,
                      flags: int) -> None:
            ...
    else:
        def _set_mode(self, **kwargs) -> None:
            self.surface = pygame.display.set_mode(**kwargs)
            logger.success(
                "Window set_mode\n"
                f"kwargs: {kwargs}"
            )

    def _set_window_frame(self) -> None:
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)

    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.WINDOWSIZECHANGED:
            self.data.size = ivec2(event.x, event.y)
            logger.info(
                "Window event - size change\n"
                f"new size: {self.data.size}"
            )
        elif event.type == pygame.WINDOWDISPLAYCHANGED:
            self.data.display = event.display_index
            logger.info(
                "Window event - display change\n"
                f"new display: {self.data.display}"
            )

    def render(self) -> None:
        pygame.display.flip()
