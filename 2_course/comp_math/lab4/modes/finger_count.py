import cv2

from recognizer.finger_counter import FingerCounter
from modes.base import BaseMode

class FingerCountMode(BaseMode):
    def __init__(self):
        self.name = "Finger Count"
        self.finger_counter = FingerCounter()
        self.total_fingers = 0

    def begin_frame(self):
        self.total_fingers = 0

    def process_hand(self, landmarks):
        self.total_fingers += self.finger_counter.detect(landmarks)

    def draw_overlay(self, frame):
        label = f"Fingers: {self.total_fingers}"

        cv2.putText(frame, label, (20, 110), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (0, 0, 0), 10, cv2.LINE_AA)
        cv2.putText(frame, label, (20, 110), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (255, 255, 255), 5, cv2.LINE_AA)
    
    def close(self):
        pass
