import cv2
import numpy as np
import time

from modes.base import BaseMode
from recognizer.hand_checks import is_draw_hand, is_open_palm, is_fist

class PaintMode(BaseMode):
    def __init__(self):
        self.name = "Paint"
        self.canvas = None
        self.brush_color = (0, 0, 255)
        self.color_slider_width = 675
        self.color_slider_height = 80
        self.color_slider_y = 18
        self.color_slider_image = self.create_color_slider()
        self.selected_color_offset = 0
        self.brush_color = tuple(
            int(channel)
            for channel in self.color_slider_image[self.color_slider_height // 2, self.selected_color_offset]
        )
        self.brush_size_min = 6
        self.brush_size_max = 30
        self.brush_size = 15
        self.brush_slider_gap = 28
        self.brush_slider_width = 420
        self.brush_slider_height = 68
        self.brush_slider_min_thickness = 8
        self.brush_slider_max_thickness = 34
        self.selected_brush_offset = int(
            (self.brush_size - self.brush_size_min)
            / (self.brush_size_max - self.brush_size_min)
            * (self.brush_slider_width - 1)
        )
        self.eraser_radius = 80
        self.previous_point = None
        self.smoothed_point = None
        self.hand_seen = False
        self.action_mode = None
        self.detected_mode = None
        self.pending_mode = None
        self.pending_mode_started_at = None
        self.mode_switch_delay = 1.0
        self.smoothing_alpha = 0.5
        self.max_line_jump = 80
        self.draw_point = None
        self.eraser_point = None
    
    def begin_frame(self):
        self.hand_seen = False
        self.detected_mode = None
        self.draw_point = None
        self.eraser_point = None
    
    def process_hand(self, landmarks):
        if self.hand_seen:
            return

        self.hand_seen = True

        index_tip = landmarks[8]
        palm_center_x = (landmarks[0].x + landmarks[1].x + landmarks[5].x + landmarks[17].x) / 4
        palm_center_y = (landmarks[0].y + landmarks[1].y + landmarks[5].y + landmarks[17].y) / 4

        if is_draw_hand(landmarks):
            self.detected_mode = "draw"
            self.draw_point = (index_tip.x, index_tip.y)
        elif is_open_palm(landmarks):
            self.detected_mode = "move"
            self.draw_point = (index_tip.x, index_tip.y)
        elif is_fist(landmarks):
            self.detected_mode = "erase"
            self.eraser_point = (palm_center_x, palm_center_y)
    
    def draw_overlay(self, frame):
        if self.canvas is None or self.canvas.shape != frame.shape:
            self.canvas = np.zeros(frame.shape, dtype=np.uint8)

        if not self.hand_seen:
            self.action_mode = None
            self.pending_mode = None
            self.pending_mode_started_at = None
            self.previous_point = None
            self.smoothed_point = None
        elif self.detected_mode == self.action_mode:
            self.pending_mode = None
            self.pending_mode_started_at = None
        elif self.detected_mode != self.pending_mode:
            self.pending_mode = self.detected_mode
            self.pending_mode_started_at = time.monotonic()
        elif self.pending_mode_started_at is not None and time.monotonic() - self.pending_mode_started_at >= self.mode_switch_delay:
            self.action_mode = self.pending_mode
            self.pending_mode = None
            self.pending_mode_started_at = None

        current_mode = self.action_mode if self.detected_mode == self.action_mode else None
        preview_point = None
        eraser_center = None

        if not self.hand_seen or current_mode != "draw":
            self.previous_point = None

        current_point = None
        if self.draw_point is not None:
            raw_point = (
                int(self.draw_point[0] * self.canvas.shape[1]),
                int(self.draw_point[1] * self.canvas.shape[0]),
            )
            if self.smoothed_point is None:
                self.smoothed_point = raw_point
            else:
                self.smoothed_point = (
                    int(self.smoothed_point[0] * (1 - self.smoothing_alpha) + raw_point[0] * self.smoothing_alpha),
                    int(self.smoothed_point[1] * (1 - self.smoothing_alpha) + raw_point[1] * self.smoothing_alpha),
                )
            current_point = self.smoothed_point

        if current_mode == "draw" and current_point is not None:

            if self.previous_point is None:
                cv2.circle(self.canvas, current_point, self.brush_size, self.brush_color, -1)
            else:
                distance = np.hypot(
                    current_point[0] - self.previous_point[0],
                    current_point[1] - self.previous_point[1],
                )
                if distance > self.max_line_jump:
                    cv2.circle(self.canvas, current_point, self.brush_size, self.brush_color, -1)
                else:
                    cv2.line(self.canvas, self.previous_point, current_point, self.brush_color, self.brush_size * 2)

            self.previous_point = current_point
            preview_point = current_point

        elif self.detected_mode in ("move", "draw") and current_point is not None:
            if self.detected_mode == "move":
                self.update_brush_color(current_point, frame.shape[1])
                self.update_brush_size(current_point, frame.shape[1])
            preview_point = current_point

        elif current_mode == "erase" and self.eraser_point is not None:
            eraser_center = (
                int(self.eraser_point[0] * self.canvas.shape[1]),
                int(self.eraser_point[1] * self.canvas.shape[0]),
            )
            cv2.circle(self.canvas, eraser_center, self.eraser_radius, (0, 0, 0), -1)

        mask = np.any(self.canvas != 0, axis=2)
        frame[mask] = self.canvas[mask]
        if eraser_center is not None:
            cv2.circle(frame, eraser_center, self.eraser_radius, (160, 160, 160), 3)
        if preview_point is not None:
            cv2.circle(frame, preview_point, self.brush_size, self.brush_color, -1)
        self.draw_color_slider(frame)
    
    def close(self):
        self.canvas = None
        self.previous_point = None
        self.smoothed_point = None
        self.hand_seen = False
        self.action_mode = None
        self.detected_mode = None
        self.pending_mode = None
        self.pending_mode_started_at = None
        self.draw_point = None
        self.eraser_point = None

    def create_color_slider(self):
        hsv_slider = np.zeros((self.color_slider_height, self.color_slider_width, 3), dtype=np.uint8)

        for x in range(self.color_slider_width):
            hue = int((x / (self.color_slider_width - 1)) * 179)
            hsv_slider[:, x] = (hue, 255, 255)

        return cv2.cvtColor(hsv_slider, cv2.COLOR_HSV2BGR)

    def get_color_slider_x(self, frame_width):
        total_width = self.color_slider_width + self.brush_slider_gap + self.brush_slider_width
        return (frame_width - total_width) // 2 + 160

    def get_brush_slider_geometry(self, frame_width):
        slider_left = self.get_color_slider_x(frame_width) + self.color_slider_width + self.brush_slider_gap
        slider_top = self.color_slider_y + (self.color_slider_height - self.brush_slider_height) // 2
        slider_bottom = slider_top + self.brush_slider_height
        slider_right = slider_left + self.brush_slider_width
        return slider_left, slider_top, slider_right, slider_bottom

    def update_brush_color(self, current_point, frame_width):
        x, y = current_point
        slider_left = self.get_color_slider_x(frame_width)

        inside_slider = (
            slider_left <= x <= slider_left + self.color_slider_width
            and self.color_slider_y <= y <= self.color_slider_y + self.color_slider_height
        )

        if inside_slider:
            local_x = x - slider_left
            local_x = max(0, min(local_x, self.color_slider_width - 1))
            self.selected_color_offset = local_x
            self.brush_color = tuple(int(channel) for channel in self.color_slider_image[self.color_slider_height // 2, local_x])

    def update_brush_size(self, current_point, frame_width):
        x, y = current_point
        slider_left, slider_top, slider_right, slider_bottom = self.get_brush_slider_geometry(frame_width)

        if slider_left <= x <= slider_right and slider_top <= y <= slider_bottom:
            local_x = x - slider_left
            local_x = max(0, min(local_x, self.brush_slider_width - 1))
            self.selected_brush_offset = local_x

            ratio = local_x / (self.brush_slider_width - 1)
            self.brush_size = int(
                self.brush_size_min + ratio * (self.brush_size_max - self.brush_size_min)
            )

    def draw_color_slider(self, frame):
        slider_top = self.color_slider_y
        slider_bottom = self.color_slider_y + self.color_slider_height
        slider_left = self.get_color_slider_x(frame.shape[1])
        slider_right = slider_left + self.color_slider_width
        selected_color_x = slider_left + self.selected_color_offset

        frame[slider_top:slider_bottom, slider_left:slider_right] = self.color_slider_image
        cv2.rectangle(frame, (slider_left, slider_top), (slider_right, slider_bottom), (40, 40, 40), 2)
        cv2.line(
            frame,
            (selected_color_x, slider_top - 8),
            (selected_color_x, slider_bottom + 8),
            (255, 255, 255),
            3,
        )

        brush_left, brush_top, brush_right, brush_bottom = self.get_brush_slider_geometry(frame.shape[1])
        brush_center_y = brush_top + self.brush_slider_height // 2

        points = np.array(
            [
                [brush_left, brush_center_y],
                [brush_right, brush_top],
                [brush_right, brush_bottom],
            ],
            dtype=np.int32,
        )
        cv2.fillConvexPoly(frame, points, (190, 190, 190))
        cv2.polylines(frame, [points], True, (60, 60, 60), 2)

        selected_x = brush_left + self.selected_brush_offset
        cv2.line(
            frame,
            (selected_x, brush_top - 6),
            (selected_x, brush_bottom + 6),
            (255, 255, 255),
            3,
        )
