from tangram.models.factory import create_standard_tangram_set


def test_create_standard_tangram_set():
    pieces = create_standard_tangram_set()
    assert len(pieces) == 7
    
    names = [p.name for p in pieces]
    assert "large_triangle_1" in names
    assert "large_triangle_2" in names
    assert "medium_triangle" in names
    assert "small_triangle_1" in names
    assert "small_triangle_2" in names
    assert "square" in names
    assert "parallelogram" in names