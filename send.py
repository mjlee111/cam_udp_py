import cv2
from udp_stream import UDPStream
import psutil
import time

HOST = "192.168.0.115" 
PORT = 5000
ID = "UMI_GRIPPER_LEFT"

udp_sender = UDPStream(ID, HOST, PORT, mode="send")

udp_sender.open_camera()
print(f"[{ID}] UMI-Gripper Left Streaming now...")
udp_sender.start_send_thread()

try:
    while True:
        cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        cpu_load = psutil.cpu_percent(interval=1)
        print(f"temp: [C] {cpu_temp}")
        print(f"load: [%] {cpu_load}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"[{ID}] Stopping UMI-Gripper Left Streaming...")
    udp_sender.stop_send_thread()
    udp_sender.close_camera()

