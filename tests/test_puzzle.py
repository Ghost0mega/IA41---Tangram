import math
from tangram.models.board import Board
from tangram.models.factory import create_standard_tangram_set
from tangram.models.puzzle import Puzzle, create_square_puzzle


def test_square_puzzle_area():
    puzzle = create_square_puzzle()
    expected_area = (2 * math.sqrt(2)) ** 2  # 8.0
    assert math.isclose(puzzle.get_total_area(), expected_area, abs_tol=1e-5)


def test_square_puzzle_solved_state():
    pieces = create_standard_tangram_set()
    board = Board(pieces)
    puzzle = create_square_puzzle()

    SQRT2 = math.sqrt(2)

    # Configuration du carré
    board.place_piece_by_anchor("large_triangle_1", target_pos=(SQRT2, SQRT2), rotation_deg=135)
    board.place_piece_by_anchor("large_triangle_2", target_pos=(SQRT2, SQRT2), rotation_deg=45)
    board.place_piece_by_anchor("small_triangle_1", target_pos=(SQRT2, SQRT2), rotation_deg=225)
    board.place_piece_by_anchor("small_triangle_2", target_pos=(1.5 * SQRT2, 1.5 * SQRT2), rotation_deg=-45)
    board.place_piece_by_anchor("medium_triangle", target_pos=(2 * SQRT2, SQRT2), rotation_deg=-135)
    board.place_piece_by_anchor("square", target_pos=(SQRT2, SQRT2), rotation_deg=-45)
    board.place_piece_by_anchor("parallelogram", target_pos=(0.0, 0.0), rotation_deg=-135, flip=True)

    assert puzzle.is_solved(board) is True


def test_square_puzzle_unsolved_when_collision():
    pieces = create_standard_tangram_set()
    board = Board(pieces)
    puzzle = create_square_puzzle()

    # Placement superposé (devrait échouer)
    board.place_piece_by_anchor("large_triangle_1", target_pos=(0.0, 0.0), rotation_deg=0)
    board.place_piece_by_anchor("large_triangle_2", target_pos=(0.0, 0.0), rotation_deg=0)

    assert puzzle.is_solved(board) is False