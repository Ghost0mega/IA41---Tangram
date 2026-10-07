from tangram.models.board import Board
from tangram.models.geometry import polygons_overlap
from tangram.models.piece import Piece


def test_polygons_overlap_true():

    square1 = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    square2 = [(1.0, 1.0), (3.0, 1.0), (3.0, 3.0), (1.0, 3.0)]
    assert polygons_overlap(square1, square2) is True


def test_polygons_touching_edges_no_overlap():
    square1 = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    square2 = [(2.0, 0.0), (4.0, 0.0), (4.0, 2.0), (2.0, 2.0)]
    assert polygons_overlap(square1, square2) is False


def test_board_collisions():
    p1 = Piece("sq1", [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)], position=(0.0, 0.0))
    p2 = Piece("sq2", [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)], position=(1.0, 0.0))
    
    board = Board([p1, p2])
    collisions = board.check_collisions()
    
    assert len(collisions) == 1
    assert collisions[0] == ("sq1", "sq2")