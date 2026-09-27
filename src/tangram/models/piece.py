import math
from tangram.models.geometry import rotation_around_center, translation


class Piece:

    def __init__(
        self,
        name: str,
        vertices: list[tuple[float, float]],
        position: tuple[float, float] = (0.0, 0.0),
        rotation_deg: float = 0.0,
    ):
        self.name = name
        # Sommets locaux (forme de base)
        self.local_vertices = vertices
        # Ancrage (ex: position du premier sommet ou du centre)
        self.position = position
        # Orientation en degrés
        self.rotation_deg = rotation_deg

    def get_center(self) -> tuple[float, float]:
        """Calcule le centre des sommets locaux."""
        n = len(self.local_vertices)
        mean_x = sum(x for x, y in self.local_vertices) / n
        mean_y = sum(y for x, y in self.local_vertices) / n
        return mean_x, mean_y

    def get_world_vertices(self) -> list[tuple[float, float]]:
        """Calcule les coordonnées réelles des sommets sur le plateau après rotation et translation."""
        center = self.get_center()
        rad = math.radians(self.rotation_deg)
        world_vertices = []

        for vertex in self.local_vertices:
            # 1. Rotation autour du centre local de la pièce
            rx, ry = rotation_around_center(vertex, center, rad)
            # 2. Translation vers la position absolue sur le plateau
            wx, wy = translation((rx, ry), self.position)
            world_vertices.append((wx, wy))

        return world_vertices