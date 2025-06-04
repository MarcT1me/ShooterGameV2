from typing import Optional, final
from dataclasses import dataclass
from pathlib import Path

import Engine


@dataclass(kw_only=True)
@final
class AssetFileData(Engine.objects.ObjectData):
    type_name: str
    path: Path
    dependencies: 'Optional[list[AssetFileData]]' = None

    def __post_init__(self):
        if self.path:
            self.path = Path(self.path)

            if not self.path.exists():
                raise FileNotFoundError(f"Asset file with id: `{self.name}`, path: `{self.path}` not found")

    def __repr__(self):
        return f"AssetFileData<{self.name}>(type: `{self.type_name}`, path: `{self.path}`, deps: {self.dependencies})"

