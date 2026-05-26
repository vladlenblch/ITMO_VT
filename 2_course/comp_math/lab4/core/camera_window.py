import cv2

class CameraWindow:
    def __init__(self, window_name="Webcam", camera_id=0):
        self.window_name = window_name
        self.cap = cv2.VideoCapture(camera_id)
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            self.window_name,
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN,
        )
    
    def read_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
        return ret, frame
    
    def show(self, frame):
        cv2.imshow(self.window_name, frame)
    
    def wait_key(self):
        return cv2.waitKey(1)
    
    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
