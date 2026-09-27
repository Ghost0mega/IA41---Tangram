import math

def translation(point: tuple[float, float], vector: tuple[float, float]) -> tuple[float, float]:
    x, y = point
    dx, dy = vector
    return x + dx, y + dy

def rotation(point: tuple[float, float], angle_rad: float) -> tuple[float, float]:
    x, y = point
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a
    
    return round(new_x, 5), round(new_y, 5) # round() to avoid float errors

def rotation_around_center(point: tuple[float, float], center: tuple[float, float], angle_rad: float) -> tuple[float, float]:
    x, y = point
    cx, cy = center
    
    x_shifted, y_shifted = translation((x, y), (-cx, -cy))  # translate to origin
    
    x_rot, y_rot = rotation((x_shifted, y_shifted), angle_rad)  # rotate around origin
    
    return translation((x_rot, y_rot), (cx, cy))    # translate back to original position


def flip_horizontal_around_center(point: tuple[float, float], center: tuple[float, float]) -> tuple[float, float]:
    x, y = point
    cx, _ = center
    flipped_x = 2 * cx - x
    return flipped_x, y

def _project_polygon(vertices: list[tuple[float, float]], axis: tuple[float, float]) -> tuple[float, float]:
    """Projette un polygon sur un axe et retourne l'intervalle [min, max]."""
    dots = [x * axis[0] + y * axis[1] for x, y in vertices]
    return min(dots), max(dots)


def polygons_overlap(poly1: list[tuple[float, float]], poly2: list[tuple[float, float]], epsilon: float = 1e-6) -> bool:
    """Détermine si deux polygones convexes se chevauchent en utilisant SAT.
    
    epsilon permet d'ignorer le simple contact bord-à-bord (arêtes/sommets qui se touchent).
    """
    for poly in (poly1, poly2):
        n = len(poly)
        for i in range(n):
            p1 = poly[i]
            p2 = poly[(i + 1) % n]
            
            edge_x = p2[0] - p1[0]
            edge_y = p2[1] - p1[1]
            
            axis = (-edge_y, edge_x)
            length = math.hypot(axis[0], axis[1])
            if length == 0:
                continue
            axis = (axis[0] / length, axis[1] / length)
            
            min1, max1 = _project_polygon(poly1, axis)
            min2, max2 = _project_polygon(poly2, axis)
            
            if max1 <= min2 + epsilon or max2 <= min1 + epsilon:
                return False
                
    return True