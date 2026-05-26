import cv2
import os
import numpy as np
from collections import deque

from modes.base import BaseMode

class MemesMode(BaseMode):
    def __init__(self):
        self.name = "Memes"
        self.image_paths = [
            os.path.join("assets/memes", filename)
            for filename in sorted(os.listdir("assets/memes"))
            if filename.endswith((".png", ".jpg", ".jpeg"))
        ]
        self.current_index = 0
        self.is_showing_image = False
        self.current_image = None
        self.box_width = 912
        self.box_height = 608
        self.left_x_history = deque(maxlen=8)
        self.right_x_history = deque(maxlen=8)
        self.left_seen = False
        self.right_seen = False
        self.swipe_threshold = 0.16
        self.swipe_cooldown = 0
    
    def begin_frame(self):
        self.left_seen = False
        self.right_seen = False

        if self.swipe_cooldown > 0:
            self.swipe_cooldown -= 1
    
    def process_hand(self, landmarks, handedness):
        middle_tip = landmarks[12]

        if handedness == "Left":
            self.left_x_history.append(middle_tip.x)
            self.left_seen = True
        elif handedness == "Right":
            self.right_x_history.append(middle_tip.x)
            self.right_seen = True
    
    def draw_overlay(self, frame):
        if not self.left_seen:
            self.left_x_history.clear()

        if not self.right_seen:
            self.right_x_history.clear()

        if not self.is_showing_image:
            self.show_current_image()

        if self.swipe_cooldown > 0:
            return

        if self.is_left_hand_swipe_right():
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.show_current_image()
            self.left_x_history.clear()
            self.right_x_history.clear()
            self.swipe_cooldown = 8
            return

        if self.is_right_hand_swipe_left():
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.show_current_image()
            self.left_x_history.clear()
            self.right_x_history.clear()
            self.swipe_cooldown = 8
            return
    
    def close(self):
        if self.is_showing_image:
            cv2.destroyWindow("Memes")
            self.is_showing_image = False
            self.current_image = None
        self.left_x_history.clear()
        self.right_x_history.clear()
        self.left_seen = False
        self.right_seen = False
        self.swipe_cooldown = 0

    def hide_external_window(self):
        if self.is_showing_image:
            cv2.destroyWindow("Memes")
            self.is_showing_image = False

    def show_external_window(self):
        if self.current_image is not None and not self.is_showing_image:
            cv2.imshow("Memes", self.current_image)
            cv2.moveWindow("Memes", (1512 - self.box_width) // 2, (982 - self.box_height) // 2)
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

    def show_current_image(self):
        image_path = self.image_paths[self.current_index]
        image = cv2.imread(image_path)

        self.current_image = self.fit_image_to_box(image)
        cv2.imshow("Memes", self.current_image)
        cv2.moveWindow("Memes", (1512 - self.box_width) // 2, (982 - self.box_height) // 2)
        self.is_showing_image = True

    def is_left_hand_swipe_right(self):
        if len(self.left_x_history) < self.left_x_history.maxlen:
            return False

        return self.left_x_history[-1] - self.left_x_history[0] >= self.swipe_threshold

    def is_right_hand_swipe_left(self):
        if len(self.right_x_history) < self.right_x_history.maxlen:
            return False

        return self.right_x_history[-1] - self.right_x_history[0] <= -self.swipe_threshold
