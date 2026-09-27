import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from tangram.models.board import Board


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


def render_board(board: Board, title: str = "Tangram Board", show: bool = True):
    """Affiche le plateau avec toutes ses pièces."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Récupérer les collisions éventuelles
    collisions = board.check_collisions()
    colliding_pieces = set()
    for p1, p2 in collisions:
        colliding_pieces.add(p1)
        colliding_pieces.add(p2)

    # Tracer chaque pièce
    for name, piece in board.pieces.items():
        vertices = piece.get_world_vertices()
        
        # Si la pièce est en collision, contour rouge épais, sinon contour noir
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
            label=name,
        )
        ax.add_patch(polygon)

        # # Afficher le nom au centre de la pièce
        # center_x, center_y = piece.position
        # ax.text(
        #     center_x,
        #     center_y,
        #     name,
        #     horizontalalignment="center",
        #     verticalalignment="center",
        #     fontsize=8,
        #     weight="bold",
        #     color="black",
        # )

    # Ajuster les limites du graphique dynamiquement
    ax.autoscale_view()
    ax.set_aspect("equal")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.title(title, fontsize=14, weight="bold")

    if show:
        plt.show()

    return fig, ax