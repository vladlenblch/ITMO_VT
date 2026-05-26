from modes.base import BaseMode

class LandmarksOnlyMode(BaseMode):
    def __init__(self):
        self.name = "Landmarks"

    def begin_frame(self):
        pass

    def process_hand(self, landmarks):
        pass

    def draw_overlay(self, frame):
        pass

    def close(self):
        pass