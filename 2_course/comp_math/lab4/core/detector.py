from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat
import cv2

class HandDetector:
    def __init__(self, path="./assets/hand_landmarker.task", hands=2, 
                 hand_detection=0.5, hand_presence=0.5, tracking_confidence=0.5):

        base_options = python.BaseOptions(path)

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=hands,
            min_hand_detection_confidence=hand_detection,
            min_hand_presence_confidence=hand_presence,
            min_tracking_confidence=tracking_confidence
        )

        self.detector = vision.HandLandmarker.create_from_options(options)
    
    def detect(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = Image(image_format=ImageFormat.SRGB, data=image_rgb)
        return self.detector.detect(mp_image)
    
    def close(self):
        self.detector.close()
