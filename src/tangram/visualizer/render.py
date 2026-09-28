from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from tangram.models.board import Board
from tangram.models.puzzle import Puzzle

# Palette de couleurs distinctes pour les 7 pièces
PIECE_COLORS = {
    "large_triangle_1": "#E74C3C",  # Rouge
    "large_triangle_2": "#E67E22",  # Orange
    "medium_triangle": "#F1C40F",  # Jaune
    "small_triangle_1": "#2ECC71",  # Vert
    "small_triangle_2": "#1ABC9C",  # Turquoise
    "square": "#3498DB",            # Bleu
    "parallelogram": "#9B59B6",     # Violet
}


def render_board(
    board: Board,
    puzzle: Optional[Puzzle] = None,
    title: str = "Tangram Board",
    show: bool = True,
):
    """Affiche le plateau avec les pièces et la silhouette cible aux hachures fines."""
    # Épaisseur des traits de hachures (0.5 pour un rendu très fin)
    plt.rcParams["hatch.linewidth"] = 0.5

    fig, ax = plt.subplots(figsize=(8, 8))

    # 1. Détection des collisions entre pièces
    collisions = board.check_collisions()
    colliding_pieces = set()
    for p1, p2 in collisions:
        colliding_pieces.add(p1)
        colliding_pieces.add(p2)

    # 2. Rendu des pièces du Tangram (zorder=1)
    for name, piece in board.pieces.items():
        vertices = piece.get_world_vertices()

        is_colliding = name in colliding_pieces
        edge_color = "red" if is_colliding else "black"
        line_width = 2.5 if is_colliding else 1.2
        fill_color = PIECE_COLORS.get(name, "#95A5A6")

        polygon = Polygon(
            vertices,
            closed=True,
            facecolor=fill_color,
            edgecolor=edge_color,
            linewidth=line_width,
            alpha=0.85,
            zorder=1,
            label=name,
        )
        ax.add_patch(polygon)

    # 3. Rendu du puzzle Cible par-dessus avec hachures fines (zorder=2)
    if puzzle is not None:
        for target_poly in puzzle.target_polygons:
            polygon_target = Polygon(
                target_poly,
                closed=True,
                fill=False,
                edgecolor="black",      # Contour noir
                linewidth=2.0,          # Contour principal
                hatch="//",             # Hachures
                zorder=2,
            )
            ax.add_patch(polygon_target)

    # 4. Ajustements d'affichage des axes et de la grille
    ax.autoscale_view()
    ax.set_aspect("equal")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.title(title, fontsize=14, weight="bold")

    if show:
        plt.show()

    return fig, ax