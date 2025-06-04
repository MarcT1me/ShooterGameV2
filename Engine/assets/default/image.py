from typing import Optional, IO

import pygame

import Engine
from Engine.assets.asset_loader import AssetLoader


class ImageAssetLoader(AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> IO[bytes]:
        return asset_file.path.open(mode="br")

    def create(self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'Optional[list[Engine.assets.AssetData]]',
               content: IO[bytes]) -> 'Engine.assets.AssetData':
        return Engine.assets.AssetData(
            name=asset_file.name,
            type_name=asset_file.type_name,
            content=pygame.image.load(content)
        )
