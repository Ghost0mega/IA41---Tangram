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
    
    # Sans rotation, les sommets sont simplement décalés de (2, 3)
    world_v = square.get_world_vertices()
    expected = [(2.0, 3.0), (3.0, 3.0), (3.0, 4.0), (2.0, 4.0)]
    assert world_v == expected


def test_piece_rotation_90_degrees():
    vertices = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    square = Piece("carre", vertices, rotation_deg=90.0)
    
    # Rotation de 90° autour du centre (1, 1)
    world_v = square.get_world_vertices()
    # Le sommet (0,0) pivote autour de (1,1) pour arriver en (2,0)
    assert world_v[0] == (2.0, 0.0)