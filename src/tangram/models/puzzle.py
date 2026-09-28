from dataclasses import dataclass
import math
from tangram.models.board import Board
from tangram.models.geometry import polygon_area


def point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]], tol: float = 1e-3) -> bool:
    """Vérifie si un point se trouve à l'intérieur ou sur le bord d'un polygone (Ray-casting)."""
    x, y = point
    n = len(polygon)
    inside = False

    px1, py1 = polygon[0]
    for i in range(n + 1):
        px2, py2 = polygon[i % n]
        
        # Vérification si le point est exactement sur un segment (gestion des bords avec tolérance)
        dx, dy = px2 - px1, py2 - py1
        if abs(dx * (y - py1) - dy * (x - px1)) < tol:
            if min(px1, px2) - tol <= x <= max(px1, px2) + tol and min(py1, py2) - tol <= y <= max(py1, py2) + tol:
                return True

        # Ray-casting standard
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                    if px1 == px2 or x <= xinters + tol:
                        inside = not inside
        px1, py1 = px2, py2

    return inside


@dataclass
class Puzzle:
    name: str
    target_polygons: list[list[tuple[float, float]]]

    def get_total_area(self) -> float:
        """Calcule l'aire totale de la silhouette cible."""
        return sum(polygon_area(poly) for poly in self.target_polygons)

    def is_solved(self, board: Board, tolerance: float = 1e-3) -> bool:
        """Vérifie si le puzzle est totalement résolu."""
        # 1. Pas de collision entre les pièces
        if board.has_collisions():
            return False

        # 2. Vérifier que TOUS les sommets de TOUTES les pièces sont dans la silhouette
        for piece in board.pieces.values():
            for vertex in piece.get_world_vertices():
                # Le sommet doit être dans au moins un des polygones cibles
                in_target = any(
                    point_in_polygon(vertex, poly, tol=tolerance)
                    for poly in self.target_polygons
                )
                if not in_target:
                    return False

        # 3. Vérifier que l'aire totale des pièces correspond à l'aire de la cible
        total_pieces_area = sum(
            polygon_area(piece.get_world_vertices()) for piece in board.pieces.values()
        )

        return math.isclose(total_pieces_area, self.get_total_area(), abs_tol=tolerance)


def create_square_puzzle() -> Puzzle:
    r"""Génère le puzzle par défaut : le Carré 2\sqrt{2} x 2\sqrt{2}."""
    side = 2.0 * math.sqrt(2)
    square_silhouette = [(0.0, 0.0), (side, 0.0), (side, side), (0.0, side)]
    return Puzzle(name="Carré Classique", target_polygons=[square_silhouette])