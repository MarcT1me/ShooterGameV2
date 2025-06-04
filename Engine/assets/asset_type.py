from dataclasses import dataclass

import Engine


@dataclass
class AssetType:
    type_name: str
    asset_loader: 'Engine.assets.AssetLoader'
