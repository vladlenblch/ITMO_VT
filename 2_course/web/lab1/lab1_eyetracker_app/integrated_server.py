import asyncio
import websockets
import json
import logging
from datetime import datetime
import threading
import time
from eye_tracker import EyeTracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegratedEyeTrackingServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.eye_tracker = EyeTracker()
        self.running = False
        self.current_gaze = {"x": 200, "y": 150}
        self.current_pupils = []
        self.current_pupils_camera = []
        
    async def register_client(self, websocket):
        self.clients.add(websocket)
        logger.info(f"клиент подключен")
        
    async def unregister_client(self, websocket):
        self.clients.discard(websocket)
        logger.info(f"клиент отключен")
        
    async def send_gaze_data(self, gaze_x, gaze_y):
        if not self.clients:
            return

        norm_x = gaze_x / 640
        norm_y = gaze_y / 480

        canvas_x = int((1 - norm_x) * 400)
        canvas_y = int(norm_y * 300)

        canvas_x = max(0, min(399, canvas_x))
        canvas_y = max(0, min(299, canvas_y))
        
        data = {
            "type": "gaze_update",
            "x": canvas_x,
            "y": canvas_y,
            "pupils": self.current_pupils,
            "pupils_camera": self.current_pupils_camera,
            "camera": {"w": int(640), "h": int(480)},
            "timestamp": datetime.now().isoformat()
        }
        
        message = json.dumps(data)

        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        for client in disconnected:
            await self.unregister_client(client)
    
    def eye_tracking_loop(self):
        if not self.eye_tracker.initialize_camera():
            logger.error("не удалось инициализировать камеру")
            return
            
        logger.info("eye tracking запущен")

        while self.running:
            frame = self.eye_tracker.get_frame()
            if frame is None:
                continue
                
            # детекция лица и глаз
            face_rect = self.eye_tracker.detect_face(frame)
            if face_rect is not None:
                eyes = self.eye_tracker.detect_eyes(frame, face_rect)
                
                if len(eyes) >= 2:
                  # точка взгляда
                    gaze_point = self.eye_tracker.calculate_gaze_point(eyes, face_rect, frame)
                    if gaze_point:
                        self.current_gaze["x"] = gaze_point[0]
                        self.current_gaze["y"] = gaze_point[1]

                    # обновление координат зрачков
                    try:
                        pupils_points = self.eye_tracker.detect_pupils(frame, eyes[:2])
                        # в координатах камеры 
                        self.current_pupils_camera = [{"x": int(float(px)), "y": int(float(py))} for (px, py) in pupils_points[:2]]
                        mapped = []
                        for (px, py) in pupils_points[:2]:
                            cx, cy = self.eye_tracker.map_to_canvas_coordinates(
                                (px, py), 640, 480, 400, 300
                            )
                            mapped.append({"x": int(float(cx)), "y": int(float(cy))})
                        self.current_pupils = mapped
                    except Exception:
                        self.current_pupils = []
                        self.current_pupils_camera = []
                else:
                    # 1 глаз как основа
                    if len(eyes) == 1:
                        ex, ey, ew, eh = eyes[0]
                        approx_x = int(float(ex + ew // 2))
                        approx_y = int(float(ey + eh // 2))
                        self.current_gaze["x"] = approx_x
                        self.current_gaze["y"] = approx_y
                    # сбрасываем
                    self.current_pupils = []
                    self.current_pupils_camera = []
            
            time.sleep(0.03)
        
        self.eye_tracker.release()
        logger.info("eye tracking остановлен")
    
    def check_point_in_area(self, x, y):
        center_x, center_y = 200, 150
        
        rel_x = x - center_x
        rel_y = y - center_y
        
        const = 140
        
        if rel_x >= 0 and rel_y <= 0:
            if rel_x <= const and rel_y >= -const/2 and rel_x + 2 * abs(rel_y) <= const:
                return True
        
        if rel_x >= 0 and rel_y >= 0:
            distance = (rel_x ** 2 + rel_y ** 2) ** 0.5
            if distance <= const:
                return True
        
        if rel_x <= 0 and rel_y >= 0:
            if rel_x >= -const and rel_y <= const/2:
                return True
        
        return False
    
    async def gaze_update_loop(self):
        while self.running:
            if self.clients:
                await self.send_gaze_data(
                    self.current_gaze["x"], 
                    self.current_gaze["y"]
                )
            await asyncio.sleep(0.05)

    async def handle_client(self, websocket):
        await self.register_client(websocket)

        try:
            welcome_message = {
                "type": "connection",
                "status": "connected",
                "message": "подключение к реальному eye tracker"
            }
            await websocket.send(json.dumps(welcome_message))

            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get("type") == "ping":
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "timestamp": datetime.now().isoformat()
                        }))
                except json.JSONDecodeError:
                    logger.error(f"плохой JSON: {message}")

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self):
        logger.info(f"запуск сервера на {self.host}:{self.port}")
        
        self.running = True
        self.loop = asyncio.get_event_loop()
        
        eye_thread = threading.Thread(target=self.eye_tracking_loop, daemon=True)
        eye_thread.start()
        
        server = websockets.serve(self.handle_client, self.host, self.port)
        
        try:
            await asyncio.gather(
                server,
                self.gaze_update_loop()
            )
        except KeyboardInterrupt:
            logger.info("сервер остановлен")
        finally:
            self.running = False

def main():
    server = IntegratedEyeTrackingServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        logger.info("сервер остановлен")

if __name__ == "__main__":
    main()
