from typing import Optional, Any
from dataclasses import dataclass

import Engine.objects


@dataclass(kw_only=True)
class AssetData(Engine.objects.ObjectData):
    type_name: str
    dependencies: 'Optional[list[AssetData]]' = None
    content: Any
