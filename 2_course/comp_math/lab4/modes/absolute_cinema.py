import random
import cv2
import os
import numpy as np

from recognizer.finger_counter import FingerCounter
from modes.base import BaseMode

class AbsoluteCinemaMode(BaseMode):
    def __init__(self):
        self.name = "Absolute Cinema"
        self.finger_counter = FingerCounter()
        self.total_fingers = 0
        self.image_paths = [
            os.path.join("assets/absolute_cinema", filename)
            for filename in os.listdir("assets/absolute_cinema")
            if filename.endswith((".png", ".jpg", ".jpeg"))
        ]
        self.is_showing_image = False
        self.current_image = None
        self.box_width = 912
        self.box_height = 608
    
    def begin_frame(self):
        self.total_fingers = 0
    
    def process_hand(self, landmarks):
        self.total_fingers += self.finger_counter.detect(landmarks)

    def draw_overlay(self, frame):
        if self.total_fingers == 10:
            if not self.is_showing_image:
                image_path = random.choice(self.image_paths)
                image = cv2.imread(image_path)

                self.current_image = self.fit_image_to_box(image)
                cv2.imshow("Absolute Cinema", self.current_image)
                cv2.moveWindow("Absolute Cinema", (1512 - self.box_width) // 2, (982 - self.box_height) // 2)
                self.is_showing_image = True
        else:
            self.close()

    def close(self):
        if self.is_showing_image:
            cv2.destroyWindow("Absolute Cinema")
            self.is_showing_image = False
            self.current_image = None

    def hide_external_window(self):
        if self.is_showing_image:
            cv2.destroyWindow("Absolute Cinema")
            self.is_showing_image = False

    def show_external_window(self):
        if self.current_image is not None and not self.is_showing_image:
            cv2.imshow("Absolute Cinema", self.current_image)
            cv2.moveWindow("Absolute Cinema", (1512 - self.box_width) // 2, (982 - self.box_height) // 2)
            self.is_showing_image = True

    def fit_image_to_box(self, image):
        image_height, image_width = image.shape[:2]
        scale = min(self.box_width / image_width, self.box_height / image_height)

        resized_width = int(image_width * scale)
        resized_height = int(image_height * scale)
        resized_image = cv2.resize(image, (resized_width, resized_height))

        canvas = np.zeros((self.box_height, self.box_width, 3), dtype=np.uint8)
        x_offset = (self.box_width - resized_width) // 2
        y_offset = (self.box_height - resized_height) // 2

        canvas[y_offset:y_offset + resized_height, x_offset:x_offset + resized_width] = resized_image
        return canvas
