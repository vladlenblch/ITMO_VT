import cv2
from collections import deque

from modes.base import BaseMode

class SixSevenMode(BaseMode):
    def __init__(self):
        self.name = "Six Seven"
        self.current_hands = []
        self.left_mid_y_history = deque(maxlen=12)
        self.right_mid_y_history = deque(maxlen=12)
        self.shake_threshold = 60
    
    def begin_frame(self):
        self.current_hands = []

    def process_hand(self, landmarks):
        self.current_hands.append({
            "x": landmarks[0].x,
            "draw_x": landmarks[12].x,
            "draw_y": landmarks[12].y,
            "mid_y": (landmarks[0].y + landmarks[12].y) / 2,
        })

    def draw_overlay(self, frame):
        if len(self.current_hands) != 2:
            self.left_mid_y_history.clear()
            self.right_mid_y_history.clear()
            return

        hands = sorted(self.current_hands, key=lambda hand: hand["x"])
        left_hand, right_hand = hands

        frame_height, frame_width = frame.shape[:2]

        left_mid_y = int(left_hand["mid_y"] * frame_height)
        right_mid_y = int(right_hand["mid_y"] * frame_height)

        self.left_mid_y_history.append(left_mid_y)
        self.right_mid_y_history.append(right_mid_y)

        left_is_shaking = self.is_shaking(self.left_mid_y_history)
        right_is_shaking = self.is_shaking(self.right_mid_y_history)

        if not (left_is_shaking and right_is_shaking):
            return

        left_text_position = (
            int(left_hand["draw_x"] * frame_width) - 50,
            int(left_hand["draw_y"] * frame_height) - 40,
        )
        right_text_position = (
            int(right_hand["draw_x"] * frame_width) - 25,
            int(right_hand["draw_y"] * frame_height) - 40,
        )

        cv2.putText(frame, "6", left_text_position, cv2.FONT_HERSHEY_SIMPLEX,
                    5, (0, 0, 255), 25, cv2.LINE_AA)
        cv2.putText(frame, "7", right_text_position, cv2.FONT_HERSHEY_SIMPLEX,
                    5, (0, 0, 255), 25, cv2.LINE_AA)

    def is_shaking(self, mid_y_history):
        if len(mid_y_history) < mid_y_history.maxlen:
            return False

        return max(mid_y_history) - min(mid_y_history) >= self.shake_threshold
