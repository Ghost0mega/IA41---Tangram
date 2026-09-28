import math
from tangram.models.board import Board
from tangram.models.factory import create_standard_tangram_set
from tangram.models.puzzle import create_square_puzzle
from tangram.visualizer.render import render_board

# Racine de 2 pour la précision géométrique exacte
SQRT2 = math.sqrt(2)


def main():
    pieces = create_standard_tangram_set()
    board = Board(pieces)
    puzzle = create_square_puzzle()

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

    # Vérification du statut du puzzle
    is_solved = puzzle.is_solved(board)
    print(f"{puzzle.name} : {is_solved}")

    # Rendu graphique du plateau avec la silhouette cible
    render_board(
        board=board,
        puzzle=puzzle,
        title=f"{puzzle.name} ({is_solved})",
    )


if __name__ == "__main__":
    main()