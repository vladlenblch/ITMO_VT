class BaseMode:
    def __init__(self):
        self.name = "Base"

    def begin_frame(self):
        pass

    def process_hand(self, landmarks):
        pass

    def draw_overlay(self, frame):
        pass

    def close(self):
        pass

    def hide_external_window(self):
        pass

    def show_external_window(self):
        pass
