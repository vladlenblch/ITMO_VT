import numpy as np

def calculate_angle(point1, point2, point3):
    v1 = (point1.x - point2.x, point1.y - point2.y)
    v2 = (point3.x - point2.x, point3.y - point2.y)
    
    len_v1 = np.sqrt(v1[0]**2 + v1[1]**2)
    len_v2 = np.sqrt(v2[0]**2 + v2[1]**2)
    
    if len_v1 == 0 or len_v2 == 0:
        return 0
    
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    
    cos_angle = dot_product / (len_v1 * len_v2)
    cos_angle = max(-1, min(1, cos_angle))
    
    angle = np.degrees(np.acos(cos_angle))
    
    return angle

def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
