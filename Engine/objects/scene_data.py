from dataclasses import dataclass, field

import Engine
from Engine.objects.object_data import ObjectData


@dataclass
class SceneData(ObjectData):
    camera_data: 'Engine.objects.CameraData'
    objects: 'dict[str, Engine.objects.Object]' = field(init=False, default_factory=dict)
