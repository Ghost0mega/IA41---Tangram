import math
from tangram.models.piece import Piece


def test_piece_initialization():
    vertices = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    square = Piece("carre", vertices)
    
    assert square.name == "carre"
    assert square.position == (0.0, 0.0)
    assert square.get_center() == (0.5, 0.5)


def test_piece_translation_only():
    vertices = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    square = Piece("carre", vertices, position=(2.0, 3.0))
    
    world_v = square.get_world_vertices()
    expected = [(2.0, 3.0), (3.0, 3.0), (3.0, 4.0), (2.0, 4.0)]
    assert world_v == expected


def test_piece_rotation_90_degrees():
    vertices = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    square = Piece("carre", vertices, rotation_deg=90.0)
    
    world_v = square.get_world_vertices()
    assert world_v[0] == (2.0, 0.0)

def test_piece_flip():
    vertices = [(0.0, 0.0), (2.0, 0.0), (0.0, 1.0)]
    piece = Piece("triangle", vertices, is_flipped=True)
    
    world_v = piece.get_world_vertices()
    assert round(world_v[0][0], 2) == 1.33