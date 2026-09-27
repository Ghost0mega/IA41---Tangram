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
        """Calcule les coordonnées réelles des sommets sur le plateau.
        
        La position (x, y) de la pièce correspond directement à l'emplacement
        du PREMIER point local (index 0).
        """
        # Le point pivot de rotation/flip est le premier sommet local (index 0)
        pivot = self.local_vertices[0]
        rad = math.radians(self.rotation_deg)
        world_vertices = []

        for vertex in self.local_vertices:
            pt = vertex

            # 1. Flip par rapport au pivot (premier point)
            if self.is_flipped:
                pt = flip_horizontal_around_center(pt, pivot)

            # 2. Rotation autour du pivot (premier point)
            rx, ry = rotation_around_center(pt, pivot, rad)

            # 3. Translation : décaler le pivot pour qu'il arrive exactement à self.position
            # dx = pos_x - pivot_x, dy = pos_y - pivot_y
            dx = self.position[0] - pivot[0]
            dy = self.position[1] - pivot[1]

            wx, wy = translation((rx, ry), (dx, dy))
            world_vertices.append((wx, wy))

        return world_vertices

    def get_relative_vertices(self) -> list[tuple[float, float]]:
            """Retourne les sommets locaux tournés et retournés, centrés sur (0,0)."""
            center_x, center_y = self.get_center()
            centered = [(x - center_x, y - center_y) for x, y in self.local_vertices]

            angle_rad = math.radians(self.rotation_deg)
            result = []

            for pt in centered:
                if self.is_flipped:
                    pt = flip_horizontal_around_center(pt, (0.0, 0.0))

                if self.rotation_deg != 0.0:
                    pt = rotation_around_center(pt, (0.0, 0.0), angle_rad)

                result.append(pt)

            return result