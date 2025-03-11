import cv2
from udp_stream import UDPStream

HOST = "192.168.0.115" 
PORT = 5000

udp_receiver = UDPStream(HOST, PORT, mode="recv")

while True:
    frame = udp_receiver.recv_frame()  
    if frame is None:
        continue
    frame = cv2.resize(frame, (1280, 480))
    cv2.imshow("Receiving", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
