import cv2
from udp_stream import UDPStream
import psutil

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
    
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
    cpu_load = psutil.cpu_percent(interval=1)
    print(f"temp: [C] {cpu_temp}")
    print(f"load: [%] {cpu_load}")

udp_sender.close_camera()
