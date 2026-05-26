import math
import time

import cv2


class ModeManager:
    def __init__(self, modes, default_mode_id=0):
        self.modes = modes
        self.current_mode_id = default_mode_id
        self.pointer_seen = False
        self.pointer_position = None
        self.menu_button_radius = 44
        self.menu_button_hover_started_at = None
        self.menu_open = False
        self.menu_hover_mode_id = None
        self.menu_hover_started_at = None
        self.menu_close_started_at = None
        self.hover_delay = 1.0
        self.menu_close_delay = 0.8
        self.external_window_hidden_for_menu = False

    @property
    def current_mode(self):
        return self.modes[self.current_mode_id]

    def set_mode(self, mode_id):
        if mode_id not in self.modes or mode_id == self.current_mode_id:
            return

        self.current_mode.close()
        self.current_mode_id = mode_id

    def handle_key(self, key):
        if ord("0") <= key <= ord("9"):
            self.set_mode(int(chr(key)))

    def begin_frame(self):
        self.pointer_seen = False
        self.pointer_position = None
        self.current_mode.begin_frame()

    def update_pointer(self, landmarks):
        if self.pointer_seen:
            return

        self.pointer_seen = True
        self.pointer_position = (landmarks[8].x, landmarks[8].y)

    def process_hand(self, landmarks):
        self.current_mode.process_hand(landmarks)

    def is_menu_open(self):
        return self.menu_open

    def draw(self, frame):
        was_menu_open = self.menu_open
        self.update_menu_state(frame)

        if self.menu_open and not was_menu_open:
            self.current_mode.hide_external_window()
            self.external_window_hidden_for_menu = True
        elif not self.menu_open and was_menu_open and self.external_window_hidden_for_menu:
            self.current_mode.show_external_window()
            self.external_window_hidden_for_menu = False

        if not self.menu_open:
            self.current_mode.draw_overlay(frame)
        self.draw_status(frame)
        self.draw_menu_button(frame)
        if self.menu_open:
            self.draw_mode_wheel(frame)

    def get_pointer_pixel_position(self, frame):
        if not self.pointer_seen or self.pointer_position is None:
            return None

        return (
            int(self.pointer_position[0] * frame.shape[1]),
            int(self.pointer_position[1] * frame.shape[0]),
        )

    def get_menu_button_center(self):
        return (70, 170)

    def get_mode_nodes(self, frame):
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        radius = min(frame.shape[1], frame.shape[0]) // 4
        display_names = {
            0: "Landmarks",
            1: "Fingers",
            2: "Cinema",
            3: "Help Me",
            4: "Six Seven",
            5: "Memes",
            6: "Rock",
            7: "Paint",
        }
        nodes = []
        mode_ids = list(self.modes.keys())

        for index, mode_id in enumerate(mode_ids):
            angle = -math.pi / 2 + index * (2 * math.pi / len(mode_ids))
            node_x = int(center_x + math.cos(angle) * radius)
            node_y = int(center_y + math.sin(angle) * radius)
            nodes.append(
                {
                    "mode_id": mode_id,
                    "name": display_names.get(mode_id, self.modes[mode_id].name),
                    "center": (node_x, node_y),
                    "radius": 77,
                }
            )

        return nodes

    def update_menu_state(self, frame):
        now = time.monotonic()
        pointer = self.get_pointer_pixel_position(frame)
        button_center = self.get_menu_button_center()

        if not self.menu_open:
            if pointer is None:
                self.menu_button_hover_started_at = None
                return

            if math.hypot(pointer[0] - button_center[0], pointer[1] - button_center[1]) <= self.menu_button_radius:
                if self.menu_button_hover_started_at is None:
                    self.menu_button_hover_started_at = now
                elif now - self.menu_button_hover_started_at >= self.hover_delay:
                    self.menu_open = True
                    self.menu_hover_mode_id = None
                    self.menu_hover_started_at = None
                    self.menu_close_started_at = None
            else:
                self.menu_button_hover_started_at = None

            return

        if pointer is None:
            self.menu_hover_mode_id = None
            self.menu_hover_started_at = None
            if self.menu_close_started_at is None:
                self.menu_close_started_at = now
            elif now - self.menu_close_started_at >= self.menu_close_delay:
                self.close_menu()
            return

        self.menu_close_started_at = None
        hovered_mode_id = None
        for node in self.get_mode_nodes(frame):
            if math.hypot(pointer[0] - node["center"][0], pointer[1] - node["center"][1]) <= node["radius"]:
                hovered_mode_id = node["mode_id"]
                break

        if hovered_mode_id != self.menu_hover_mode_id:
            self.menu_hover_mode_id = hovered_mode_id
            self.menu_hover_started_at = now if hovered_mode_id is not None else None
            return

        if hovered_mode_id is not None and self.menu_hover_started_at is not None:
            if now - self.menu_hover_started_at >= self.hover_delay:
                self.set_mode(hovered_mode_id)
                self.close_menu()

    def close_menu(self):
        self.menu_open = False
        self.menu_button_hover_started_at = None
        self.menu_hover_mode_id = None
        self.menu_hover_started_at = None
        self.menu_close_started_at = None

    def draw_hover_progress(self, frame, center, radius, started_at):
        if started_at is None:
            return

        progress = min((time.monotonic() - started_at) / self.hover_delay, 1.0)
        if progress <= 0:
            return

        cv2.ellipse(frame, center, (radius + 10, radius + 10), -90, 0,
                    int(progress * 360), (255, 255, 255), 5, cv2.LINE_AA)

    def draw_menu_button(self, frame):
        button_center = self.get_menu_button_center()
        pointer = self.get_pointer_pixel_position(frame)
        hovered = (
            pointer is not None
            and math.hypot(pointer[0] - button_center[0], pointer[1] - button_center[1]) <= self.menu_button_radius
        )
        fill_color = (80, 80, 80) if hovered or self.menu_open else (45, 45, 45)

        cv2.circle(frame, button_center, self.menu_button_radius, fill_color, -1, cv2.LINE_AA)
        cv2.circle(frame, button_center, self.menu_button_radius, (255, 255, 255), 3, cv2.LINE_AA)
        self.draw_hover_progress(frame, button_center, self.menu_button_radius, self.menu_button_hover_started_at)

        text_size, baseline = cv2.getTextSize("Modes", cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        text_x = button_center[0] - text_size[0] // 2
        text_y = button_center[1] + (text_size[1] - baseline) // 2

        cv2.putText(frame, "Modes", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 0), 6, cv2.LINE_AA)
        cv2.putText(frame, "Modes", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2, cv2.LINE_AA)

    def draw_mode_wheel(self, frame):
        overlay = frame.copy()
        wheel_center = (frame.shape[1] // 2, frame.shape[0] // 2)
        wheel_radius = min(frame.shape[1], frame.shape[0]) // 3
        cv2.circle(overlay, wheel_center, wheel_radius, (20, 20, 20), -1, cv2.LINE_AA)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

        cv2.circle(frame, wheel_center, wheel_radius, (255, 255, 255), 3, cv2.LINE_AA)

        for node in self.get_mode_nodes(frame):
            center = node["center"]
            radius = node["radius"]
            is_current = node["mode_id"] == self.current_mode_id
            is_hovered = node["mode_id"] == self.menu_hover_mode_id

            fill_color = (60, 60, 60)
            if is_current:
                fill_color = (60, 110, 60)
            if is_hovered:
                fill_color = (120, 120, 120)

            cv2.circle(frame, center, radius, fill_color, -1, cv2.LINE_AA)
            cv2.circle(frame, center, radius, (255, 255, 255), 3, cv2.LINE_AA)

            if is_hovered:
                self.draw_hover_progress(frame, center, radius, self.menu_hover_started_at)

            name_size, baseline = cv2.getTextSize(node["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.putText(frame, node["name"],
                        (center[0] - name_size[0] // 2, center[1] + (name_size[1] - baseline) // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2, cv2.LINE_AA)

    def draw_status(self, frame):
        mode_label = f"Mode: {self.current_mode.name}"

        cv2.putText(frame, mode_label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (0, 0, 0), 10, cv2.LINE_AA)
        cv2.putText(frame, mode_label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (255, 255, 255), 5, cv2.LINE_AA)
