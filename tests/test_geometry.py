import math
from tangram.models.geometry import translation, rotation, rotation_around_center

def test_translation():
    point = (1.0, 2.0)
    vector = (3.0, -1.0)
    assert translation(point, vector) == (4.0, 1.0)


def test_rotation_90_degrees():
    # Un point à (1, 0) tourné de 90° (pi/2) doit arriver en (0, 1)
    point = (1.0, 0.0)
    angle = math.pi / 2
    assert rotation(point, angle) == (0.0, 1.0)


def test_rotation_around_center():
    # Tourner le point (2, 1) de 90° autour du centre (1, 1) donne (1, 2)
    point = (2.0, 1.0)
    center = (1.0, 1.0)
    angle = math.pi / 2
    assert rotation_around_center(point, center, angle) == (1.0, 2.0)