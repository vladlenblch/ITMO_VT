import cv2

class HandDrawer:
    def __init__(self, line_thickness=10, point_radius=15):
        self.line_thickness = line_thickness
        self.point_radius = point_radius
        
        self.connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (1, 5), (5, 6), (6, 7), (7, 8),
            (9, 10), (10, 11), (11, 12),
            (13, 14), (14, 15), (15, 16),
            (0, 17), (17, 18), (18, 19), (19, 20),
            (5, 9), (9, 13), (13, 17)
        ]
    
    def draw(self, image, hand_landmarks):
        h, w, _ = image.shape
        
        for idx1, idx2 in self.connections:
            point1 = hand_landmarks[idx1]
            point2 = hand_landmarks[idx2]
            x1, y1 = int(point1.x * w), int(point1.y * h)
            x2, y2 = int(point2.x * w), int(point2.y * h)
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), self.line_thickness)
        
        for landmark in hand_landmarks:
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(image, (x, y), self.point_radius, (0, 0, 255), -1)
        
        return image
