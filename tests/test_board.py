import pytest
from tangram.models.board import Board
from tangram.models.factory import create_standard_tangram_set


def test_board_initialization():
    pieces = create_standard_tangram_set()
    board = Board(pieces)
    assert len(board.pieces) == 7


def test_board_add_and_remove():
    board = Board()
    pieces = create_standard_tangram_set()
    
    board.add_piece(pieces[0])
    assert "large_triangle_1" in board.pieces
    
    removed = board.remove_piece("large_triangle_1")
    assert removed.name == "large_triangle_1"
    assert "large_triangle_1" not in board.pieces


def test_board_duplicate_piece_error():
    pieces = create_standard_tangram_set()
    board = Board([pieces[0]])
    
    with pytest.raises(ValueError):
        board.add_piece(pieces[0])


def test_board_move_and_rotate():
    pieces = create_standard_tangram_set()
    board = Board(pieces)
    
    board.move_piece("square", (5.0, 5.0))
    board.rotate_piece("square", 45.0)
    
    square = board.get_piece("square")
    assert square.position == (5.0, 5.0)
    assert square.rotation_deg == 45.0