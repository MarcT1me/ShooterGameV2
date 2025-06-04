from typing import Optional, TextIO
from dataclasses import dataclass
import json

import pygame
import glm

import Engine

from core.game_scene import GameSceneData, GameScene

CONFIG_PATH = "app_data\\configs"
FONTS_PATH = "assets\\fonts"


class JsonConfigLoader(Engine.assets.AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> TextIO:
        return asset_file.path.open(mode="r")

    def create(self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'Optional[list[Engine.assets.AssetData]]',
               content: TextIO) -> 'Engine.assets.AssetData':
        return Engine.assets.AssetData(
            name=asset_file.name,
            type_name=asset_file.type_name,
            content=json.load(content)
        )


class WindowConfigData:
    def __init__(self):
        asset_manager: Engine.assets.AssetManager = Engine.App.get().asset_manager
        self._raw_window_config_data: dict = asset_manager.load(
            Engine.assets.AssetFileData(
                name="window",
                type_name="jsonConfig",
                path=CONFIG_PATH + "\\window.json"
            )
        ).content

        self._window_data = Engine.window.WinData(
            size=glm.vec2(*self._raw_window_config_data["size"]),
            vsync=self._raw_window_config_data["vsync"],
            display=self._raw_window_config_data["display"],
            full_mode=Engine.window.FullMode.__dict__.get(self._raw_window_config_data["full_mode"]),
            clear_color=glm.ivec4(0.1 * 255, 0.3 * 255, 0.3 * 255, 1.0 * 255)
        )

    @property
    def win_data(self) -> Engine.window.WinData:
        return self._window_data

    @property
    def fps(self) -> int:
        return self._raw_window_config_data["fps"]


@dataclass
class ShooterGameData(Engine.app.AppData):
    is_release: bool = False


class ShooterGameV2(Engine.App):
    data: ShooterGameData

    def prepare_instance(self) -> 'Engine.app.AppData':
        window_config: WindowConfigData = WindowConfigData()

        return ShooterGameData(
            name="ShooterGame v2",
            win_data=window_config.win_data,
            clock_data=Engine.time.ClockData(
                tps=window_config.fps
            ),
            # game data
        )

    def __init__(self):
        super().__init__()

        self.font = pygame.font.SysFont("Arial", 30)
        self.rnd_fps_font = self.font.render("FPS: 0", True, "white")

        self.clock.add_defer(
            defer=Engine.time.Timer("fps updater", 1 / 3),
            category="timer"
        )

        self.scene: GameScene = GameScene(
            GameSceneData(
                name="scene",
                camera_data=Engine.objects.game_object.GameObjectData(
                    name="camera",
                    transform=Engine.objects.game_object.Transform(
                        position=glm.vec2(0),
                        direction=None
                    )
                ),
                player_speed=0.125,
            )
        )

        self.scene.add_objects()

    def reload_data(self, data: 'Engine.objects.ObjectData'):
        window_config: WindowConfigData = WindowConfigData()

        self.window.reload_data(window_config.win_data)

        self.clock.data.tps = window_config.fps

    def event(self, event: pygame.event.Event) -> None:
        self.scene.event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.key == pygame.K_r:
                self.reload_data(self.data)

    def update(self, delta_time: float) -> None:
        self.scene.update(delta_time)

        if self.clock.timer("fps updater"):
            self.rnd_fps_font = self.font.render(f"FPS: {int(self.clock.get_tps())}", True, "white")

    def render(self) -> None:
        self.scene.render()

        self.window.surface.blit(self.rnd_fps_font, (0, 0))


if __name__ == "__main__":
    Engine.App.reg_asset_types.extend(
        [
            Engine.assets.AssetType(
                type_name="jsonConfigХ",
                asset_loader=JsonConfigLoader()
            )
        ]
    )

    ShooterGameV2().start()
