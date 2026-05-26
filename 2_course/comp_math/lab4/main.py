import time

from core.detector import HandDetector
from core.drawer import HandDrawer

from modes.manager import ModeManager
from modes.landmarks_only import LandmarksOnlyMode
from modes.finger_count import FingerCountMode
from modes.absolute_cinema import AbsoluteCinemaMode
from modes.help_me import HelpMeMode
from modes.six_seven import SixSevenMode
from modes.memes import MemesMode
from modes.rock import RockMode
from modes.paint import PaintMode

from core.camera_window import CameraWindow
from recognizer.hand_checks import is_exit_hand

def main():
    hand_detector = HandDetector()
    hand_drawer = HandDrawer()
    camera_window = CameraWindow()

    mode_manager = ModeManager(
        modes={
            0: LandmarksOnlyMode(),
            1: FingerCountMode(),
            2: AbsoluteCinemaMode(),
            3: HelpMeMode(),
            4: SixSevenMode(),
            5: MemesMode(),
            6: RockMode(),
            7: PaintMode(),
        },
        default_mode_id=0,
    )
    exit_gesture_started_at = None
    
    while True:
        ret, frame = camera_window.read_frame()
        should_exit = False
 
        if ret:
            results = hand_detector.detect(frame)
            mode_manager.begin_frame()

            if results.hand_landmarks:
                handedness_list = results.handedness or [None] * len(results.hand_landmarks)

                for hand_landmarks, handedness in zip(results.hand_landmarks, handedness_list):
                    mode_manager.update_pointer(hand_landmarks)

                    if is_exit_hand(hand_landmarks):
                        if exit_gesture_started_at is None:
                            exit_gesture_started_at = time.monotonic()
                        elif time.monotonic() - exit_gesture_started_at >= 1.0:
                            should_exit = True
                        break

                    if mode_manager.is_menu_open():
                        continue

                    if mode_manager.current_mode_id == 0:
                        hand_drawer.draw(frame, hand_landmarks)
                    elif mode_manager.current_mode_id == 5:
                        handedness_name = handedness[0].category_name if handedness else None
                        mode_manager.current_mode.process_hand(hand_landmarks, handedness_name)
                    else:
                        mode_manager.process_hand(hand_landmarks)
                else:
                    exit_gesture_started_at = None
            else:
                exit_gesture_started_at = None

            if should_exit:
                break

            mode_manager.draw(frame)
            camera_window.show(frame)

            key = camera_window.wait_key()
            mode_manager.handle_key(key)

        if should_exit:
            break

    hand_detector.close()
    camera_window.close()

if __name__ == "__main__":
    main()
