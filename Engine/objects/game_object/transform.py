from dataclasses import dataclass

import glm


@dataclass
class Transform:
    position: glm.vec2
    direction: glm.vec2

    def move_to(self, position: glm.vec2) -> glm.vec2:
        self.position += position
        return self.position

    def set_direction(self, rotation: glm.vec2) -> glm.vec2:
        self.direction = rotation
        return self.direction

    def get_angle_deg(self) -> float:
        return glm.degrees(self.get_angle_rad()) % 360

    def get_angle_rad(self) -> float:
        return glm.atan(self.direction.y, self.direction.x)
