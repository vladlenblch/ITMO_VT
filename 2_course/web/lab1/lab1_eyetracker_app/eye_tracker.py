import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EyeTracker:    
    def __init__(self):
        self.cap = None
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = None
        
        self.LEFT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.RIGHT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.LEFT_IRIS_INDICES = [468, 469, 470, 471, 472]
        self.RIGHT_IRIS_INDICES = [473, 474, 475, 476, 477]
        
        self.gaze_smoothing_alpha = 0.3
        self.smoothed_gaze = None
        
    def initialize_camera(self, camera_index: int = 0) -> bool:
        try:
            if self.cap is not None:
                self.cap.release()
                cv2.destroyAllWindows()
            
            for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
                try:
                    self.cap = cv2.VideoCapture(camera_index, backend)
                    if self.cap.isOpened():
                        break
                except:
                    continue
            else:
                self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"камера не открывается")
                return False
                
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            ret, _ = self.cap.read()
            if not ret:
                logger.error("не получается достать кадр")
                self.cap.release()
                return False
            
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
            logger.info("eye tracker инициализирован с MediaPipe")
            return True
            
        except Exception as e:
            logger.error(f"ошибка инициализации: {e}")
            if self.cap is not None:
                self.cap.release()
            return False
    
    def get_frame(self) -> Optional[np.ndarray]:
        if self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            logger.warning("не получается достать кадр")
            return None
            
        return frame
    
    def detect_face(self, frame: np.ndarray) -> Optional[List]:
        if self.face_mesh is None:
            return None
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            # лицо
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            
            # квадрат лица
            x_coords = [landmark.x * w for landmark in face_landmarks.landmark]
            y_coords = [landmark.y * h for landmark in face_landmarks.landmark]
            
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            
            return [x_min, y_min, x_max - x_min, y_max - y_min]
        
        return None
    
    def detect_eyes(self, frame: np.ndarray, face_rect: List) -> List:
        if self.face_mesh is None:
            return []
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        eyes = []
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            
            # левый глаз
            left_eye_points = [(int(face_landmarks.landmark[i].x * w), 
                               int(face_landmarks.landmark[i].y * h)) 
                              for i in self.LEFT_EYE_INDICES]
            if left_eye_points:
                x_coords = [p[0] for p in left_eye_points]
                y_coords = [p[1] for p in left_eye_points]
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                eyes.append((x_min, y_min, x_max - x_min, y_max - y_min))
            
            # правый глаз
            right_eye_points = [(int(face_landmarks.landmark[i].x * w), 
                                int(face_landmarks.landmark[i].y * h)) 
                               for i in self.RIGHT_EYE_INDICES]
            if right_eye_points:
                x_coords = [p[0] for p in right_eye_points]
                y_coords = [p[1] for p in right_eye_points]
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                eyes.append((x_min, y_min, x_max - x_min, y_max - y_min))
        
        return eyes
    
    def detect_pupils(self, frame: np.ndarray, eyes: List) -> List[Tuple[int, int]]:
        if self.face_mesh is None:
            return []
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        pupils = []
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            
            # центр радужки левого зрачка
            left_iris_points = [(int(face_landmarks.landmark[i].x * w), 
                                int(face_landmarks.landmark[i].y * h)) 
                               for i in self.LEFT_IRIS_INDICES]
            if left_iris_points:
                left_pupil_x = int(np.mean([p[0] for p in left_iris_points]))
                left_pupil_y = int(np.mean([p[1] for p in left_iris_points]))
                pupils.append((left_pupil_x, left_pupil_y))
            
            # центр радужки правого зрачка
            right_iris_points = [(int(face_landmarks.landmark[i].x * w), 
                                 int(face_landmarks.landmark[i].y * h)) 
                                for i in self.RIGHT_IRIS_INDICES]
            if right_iris_points:
                right_pupil_x = int(np.mean([p[0] for p in right_iris_points]))
                right_pupil_y = int(np.mean([p[1] for p in right_iris_points]))
                pupils.append((right_pupil_x, right_pupil_y))
        
        return pupils
    
    def calculate_gaze_point(self, eyes: List, face_rect: List, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        if len(eyes) < 2 or face_rect is None:
            return None
        
        eyes_sorted = sorted(eyes, key=lambda eye: eye[0])
        left_eye = eyes_sorted[0]
        right_eye = eyes_sorted[1]
        
        pupils = self.detect_pupils(frame, [left_eye, right_eye])
        
        if len(pupils) < 2:
            left_pupil = (left_eye[0] + left_eye[2] // 2, left_eye[1] + left_eye[3] // 2)
            right_pupil = (right_eye[0] + right_eye[2] // 2, right_eye[1] + right_eye[3] // 2)
        else:
            left_pupil = pupils[0]
            right_pupil = pupils[1]
        
        left_eye_center = (left_eye[0] + left_eye[2] // 2, left_eye[1] + left_eye[3] // 2)
        right_eye_center = (right_eye[0] + right_eye[2] // 2, right_eye[1] + right_eye[3] // 2)
        
        left_offset_x = left_pupil[0] - left_eye_center[0]
        left_offset_y = left_pupil[1] - left_eye_center[1]
        
        right_offset_x = right_pupil[0] - right_eye_center[0]
        right_offset_y = right_pupil[1] - right_eye_center[1]
        
        avg_offset_x = (left_offset_x + right_offset_x) / 2
        avg_offset_y = (left_offset_y + right_offset_y) / 2
        
        eye_center_x = (left_eye_center[0] + right_eye_center[0]) // 2
        eye_center_y = (left_eye_center[1] + right_eye_center[1]) // 2
        
        scale_factor = 30.0
        
        gaze_x = int(eye_center_x + avg_offset_x * scale_factor)
        gaze_y = int(eye_center_y + avg_offset_y * scale_factor)
        
        frame_height, frame_width = frame.shape[:2]
        gaze_x = max(0, min(frame_width - 1, gaze_x))
        gaze_y = max(0, min(frame_height - 1, gaze_y))
        
        if self.smoothed_gaze is None:
            self.smoothed_gaze = (gaze_x, gaze_y)
        else:
            smoothed_x = int(self.smoothed_gaze[0] * (1 - self.gaze_smoothing_alpha) + gaze_x * self.gaze_smoothing_alpha)
            smoothed_y = int(self.smoothed_gaze[1] * (1 - self.gaze_smoothing_alpha) + gaze_y * self.gaze_smoothing_alpha)
            self.smoothed_gaze = (smoothed_x, smoothed_y)
        
        return self.smoothed_gaze
    
    def map_to_canvas_coordinates(self, gaze_point: Tuple[int, int], 
                                camera_width: int, camera_height: int,
                                canvas_width: int, canvas_height: int) -> Tuple[int, int]:
        if gaze_point is None:
            return (canvas_width // 2, canvas_height // 2)
        
        norm_x = gaze_point[0] / camera_width
        norm_y = gaze_point[1] / camera_height
        
        canvas_x = int(norm_x * canvas_width)
        canvas_y = int(norm_y * canvas_height)
        
        canvas_x = max(0, min(canvas_width - 1, canvas_x))
        canvas_y = max(0, min(canvas_height - 1, canvas_y))
        
        return (canvas_x, canvas_y)
    
    def draw_face_and_eyes(self, frame: np.ndarray, face_rect: List, eyes: List) -> np.ndarray:
        annotated_frame = frame.copy()
        
        if face_rect is not None:
            x, y, w, h = face_rect
            cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(annotated_frame, "Face", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        for i, (ex, ey, ew, eh) in enumerate(eyes):
            cv2.rectangle(annotated_frame, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            cv2.putText(annotated_frame, f"Eye {i+1}", (ex, ey-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        if len(eyes) >= 2:
            pupils = self.detect_pupils(frame, eyes)
            for i, pupil in enumerate(pupils):
                cv2.circle(annotated_frame, pupil, 3, (255, 255, 0), -1)  # Желтые зрачки
                cv2.putText(annotated_frame, f"P{i+1}", (pupil[0] + 5, pupil[1] - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)
        
        gaze_point = self.calculate_gaze_point(eyes, face_rect, frame)
        if gaze_point:
            cv2.circle(annotated_frame, gaze_point, 8, (0, 0, 255), -1)
            cv2.putText(annotated_frame, "Gaze", (gaze_point[0] + 10, gaze_point[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        return annotated_frame
    
    def release(self):
        try:
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            
            if self.face_mesh is not None:
                self.face_mesh.close()
                self.face_mesh = None
            
            cv2.destroyAllWindows()
            
            import time
            time.sleep(0.1)
            
            logger.info("камера освободилась")
        except Exception as e:
            logger.error(f"ошибка: {e}")
            self.cap = None
