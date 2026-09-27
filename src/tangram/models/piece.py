import math
from tangram.models.geometry import (
    flip_horizontal_around_center,
    rotation_around_center,
    translation,
)


class Piece:

    def __init__(
        self,
        name: str,
        vertices: list[tuple[float, float]],
        position: tuple[float, float] = (0.0, 0.0),
        rotation_deg: float = 0.0,
        is_flipped: bool = False,
    ):
        self.name = name
        self.local_vertices = vertices
        self.position = position
        self.rotation_deg = rotation_deg
        self.is_flipped = is_flipped

    def get_center(self) -> tuple[float, float]:
        """Calcule le centre des sommets locaux."""
        n = len(self.local_vertices)
        mean_x = sum(x for x, y in self.local_vertices) / n
        mean_y = sum(y for x, y in self.local_vertices) / n
        return mean_x, mean_y

    def flip(self):
        """Bascule l'état miroir de la pièce."""
        self.is_flipped = not self.is_flipped

    def get_world_vertices(self) -> list[tuple[float, float]]:
        """Calcule les coordonnées réelles des sommets sur le plateau."""
        center = self.get_center()
        rad = math.radians(self.rotation_deg)
        world_vertices = []

        for vertex in self.local_vertices:
            pt = vertex

            if self.is_flipped:
                pt = flip_horizontal_around_center(pt, center)

            rx, ry = rotation_around_center(pt, center, rad)

            wx, wy = translation((rx, ry), self.position)
            world_vertices.append((wx, wy))

        return world_vertices