from tangram.models.piece import Piece


def create_standard_tangram_set() -> list[Piece]:
    """Génère le jeu standard des 7 pièces du Tangram."""
    return [
        Piece("large_triangle_1", [(0.0, 0.0), (2.0, 0.0), (0.0, 2.0)]),
        Piece("large_triangle_2", [(0.0, 0.0), (2.0, 0.0), (0.0, 2.0)]),

        Piece("medium_triangle", [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0)]),
        Piece("small_triangle_1", [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),
        Piece("small_triangle_2", [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),

        Piece("square", [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]),

        Piece("parallelogram", [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (1.0, 1.0)]),
    ]