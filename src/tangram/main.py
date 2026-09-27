from tangram.models.board import Board
from tangram.models.factory import create_standard_tangram_set
from tangram.visualizer.render import render_board
import math

# Racine de 2 pour la précision géométrique exacte
SQRT2 = math.sqrt(2)  # approx 1.41421356


def main():
    pieces = create_standard_tangram_set()
    board = Board(pieces)

    board.place_piece_by_anchor(
        "large_triangle_1", target_pos=(SQRT2, SQRT2), rotation_deg=135
    )

    board.place_piece_by_anchor(
        "large_triangle_2", target_pos=(SQRT2, SQRT2), rotation_deg=45
    )

    board.place_piece_by_anchor(
        "small_triangle_1", target_pos=(SQRT2, SQRT2), rotation_deg=225
    )

    board.place_piece_by_anchor(
        "small_triangle_2", target_pos=(1.5 * SQRT2, 1.5 * SQRT2), rotation_deg=-45
    )

    board.place_piece_by_anchor(
        "medium_triangle", target_pos=(2 * SQRT2, SQRT2), rotation_deg=-135
    )

    board.place_piece_by_anchor(
        "square", target_pos=(SQRT2, SQRT2), rotation_deg=-45
    )

    board.place_piece_by_anchor(
        "parallelogram", target_pos=(0.0, 0.0), rotation_deg=-135, flip=True
    )

    # Rendu graphique du plateau
    render_board(board, title="Tangram")


if __name__ == "__main__":
    main()