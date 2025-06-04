from dataclasses import dataclass

import glm
import pygame

import Engine

import core


@dataclass
class GameSceneData(Engine.objects.SceneData):
    player_speed: float


class GameScene(Engine.objects.Scene):
    data: GameSceneData

    def __init__(self, data: GameSceneData):
        super().__init__(data)
        self.load_assets()

    def load_assets(self):
        self.app.asset_manager.load(
            asset_file=Engine.assets.AssetFileData(
                name="player",
                type_name="image",
                path="assets\\player\\player.png"
            )
        )
        self.app.asset_manager.load(
            asset_file=Engine.assets.AssetFileData(
                name="assault_rifle",
                type_name="image",
                path="assets\\weapons\\assault_rifle\\assault_rifle.png"
            )
        )
        self.app.asset_manager.load(
            asset_file=Engine.assets.AssetFileData(
                name="scar_l",
                type_name="image",
                path="assets\\weapons\\scar_l\\scar_l.png"
            )
        )
        self.app.asset_manager.load(
            asset_file=Engine.assets.AssetFileData(
                name="shotgun",
                type_name="image",
                path="assets\\weapons\\shotgun\\shotgun.png"
            )
        )

    def add_objects(self):
        # player
        player = core.objects.Player(
            core.objects.PlayerData(
                name=Engine.get_identifier(),
                transform=Engine.objects.game_object.Transform(
                    position=glm.vec2(100),
                    direction=glm.vec2(0)
                ),
                speed=self.data.player_speed
            )
        )
        self.add_object(player)

        # assault_rifle
        assault_rifle = core.objects.weapons.AssaultRifle(
            core.objects.weapons.AssaultRifleData(
                name=Engine.get_identifier(),
                transform=Engine.objects.game_object.Transform(
                    position=player.data.transform.position.xy,
                    direction=player.data.transform.direction.xy
                )
            )
        )
        assault_rifle.drop()
        self.add_object(assault_rifle)

        # scar_l
        scar_l = core.objects.weapons.MarksmanRifle(
            core.objects.weapons.MarksmanRifleData(
                name=Engine.get_identifier(),
                transform=Engine.objects.game_object.Transform(
                    position=player.data.transform.position.xy,
                    direction=player.data.transform.direction.xy
                )
            )
        )
        scar_l.drop()
        self.add_object(scar_l)

        # shotgun
        shotgun = core.objects.weapons.ShotGun(
            core.objects.weapons.ShotGunData(
                name=Engine.get_identifier(),
                transform=Engine.objects.game_object.Transform(
                    position=player.data.transform.position.xy,
                    direction=player.data.transform.direction.xy
                )
            )
        )
        shotgun.pickup(player.data)
        self.add_object(shotgun)

    def event(self, event: pygame.event.Event) -> None:
        if event.type == core.objects.BULLET_IMPACT_EVENT:
            bullet: core.objects.Bullet = self.pop_object(event.name)
            impact_target = event.impact_target
            if impact_target is not None:
                impact_object = self.get_object(impact_target)
                if isinstance(impact_object, Engine.objects.Object):
                    print(f"the object {impact_object.data.name} hit and damaged on {bullet.data.damage}")

        super().event(event)
