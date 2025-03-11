import cv2
import socket
import struct
import numpy as np
import threading

class UDPStream:
    def __init__(self, host, port, mode="send"):
        self.host = host
        self.port = port
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        if mode == "recv":
            print("UDP receiver node initialized")
            self.sock.bind((host, port))
            self.frame = None
            self.recv_thread = None
            self.running = False
        else:
            print("UDP sender node initialized")

    def start_recv_thread(self):
        print("Starting UDP receiver thread")
        self.running = True
        self.recv_thread = threading.Thread(target=self.recv_frame)
        self.recv_thread.start()
        
    def stop_recv_thread(self):
        print("Stopping UDP receiver thread")
        if self.recv_thread:
            self.running = False
            self.recv_thread.join()
            self.recv_thread = None

    def send_frame(self, frame):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, buffer = cv2.imencode(".jpg", frame, encode_param)
        self.sock.sendto(buffer.tobytes(), (self.host, self.port))

    def recv_frame(self):
        while self.running:
            data, _ = self.sock.recvfrom(65536)
            np_arr = np.frombuffer(data, dtype=np.uint8)
            self.frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    def open_camera(self, camera_id=0, width=1280, height=480, fps=15):
        print(f"Trying to open camera {camera_id}")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Failed to open camera.")
            exit()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        print(f"Camera {camera_id} opened with {width}x{height} at {fps} fps")
        
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read frame.")
            return None
        return frame

    def close_camera(self):
        self.cap.release()
        print("Camera closed")
            
