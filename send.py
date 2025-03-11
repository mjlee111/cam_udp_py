import cv2
from udp_stream import UDPStream

HOST = "localhost" 
PORT = 5000

udp_sender = UDPStream(HOST, PORT, mode="send")

cap = cv2.VideoCapture(0)  
if cap.isOpened():
    print(f"Successfully opened camera {0}")
else:
    print("Failed to open camera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (640, 240))
    udp_sender.send_frame(frame)  

    cv2.imshow("Sending", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
