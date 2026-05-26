import cv2

from recognizer.finger_counter import FingerCounter
from modes.base import BaseMode

class HelpMeMode(BaseMode):
    def __init__(self):
        self.name = "Help Me"
        self.finger_counter = FingerCounter()
        self.total_fingers = 0
        self.hand_detected = False
        self.is_showing_image = False
        self.current_image = None
    
    def begin_frame(self):
        self.total_fingers = 0
        self.hand_detected = False
    
    def process_hand(self, landmarks):
        self.hand_detected = True
        self.total_fingers += self.finger_counter.detect(landmarks)
    
    def draw_overlay(self, frame):        
        if self.hand_detected and self.total_fingers == 0:
            if not self.is_showing_image:
                self.current_image = cv2.imread("assets/help/cat_girl.png")

                cv2.imshow("Help Me", self.current_image)
                cv2.moveWindow("Help Me", 525, 190)
                self.is_showing_image = True
        else:
            self.close()
    
    def close(self):
        if self.is_showing_image:
            cv2.destroyWindow("Help Me")
            self.is_showing_image = False
            self.current_image = None

    def hide_external_window(self):
        if self.is_showing_image:
            cv2.destroyWindow("Help Me")
            self.is_showing_image = False

    def show_external_window(self):
        if self.current_image is not None and not self.is_showing_image:
            cv2.imshow("Help Me", self.current_image)
            cv2.moveWindow("Help Me", 525, 190)
            self.is_showing_image = True
