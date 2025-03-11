import cv2
from udp_stream import UDPStream

HOST = "192.168.0.115" 
PORT = 5000

udp_sender = UDPStream(HOST, PORT, mode="send")

udp_sender.open_camera()
print("UMI-Gripper Left Streaming now...")

while True:
    frame = udp_sender.get_frame()
    if frame is None:
        continue
    
    frame = cv2.resize(frame, (640, 240))
    udp_sender.send_frame(frame)

udp_sender.close_camera()
