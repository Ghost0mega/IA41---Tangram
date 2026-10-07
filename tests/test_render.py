from tangram.models.board import Board
from tangram.models.factory import create_standard_tangram_set
from tangram.visualizer.render import render_board


def test_render_board_execution():
    pieces = create_standard_tangram_set()
    board = Board(pieces)
    
    # S'assurer que le rendu ne lève aucune exception
    fig, ax = render_board(board, show=False)
    assert fig is not None
    assert ax is not None