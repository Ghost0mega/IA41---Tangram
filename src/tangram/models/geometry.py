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