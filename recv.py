import cv2
import sys
import time
from udp_stream import UDPStream

HOST = "192.168.0.115" 
PORT = 5000
ID = "UMI_GRIPPER_LEFT"

udp_receiver = None

try:
    udp_receiver = UDPStream(ID, HOST, PORT, mode="recv")
    udp_receiver.start_recv_thread()    

    while True:
        try:
            frame = udp_receiver.frame
            if frame is not None:
                frame = cv2.resize(frame, (1280, 480))
                cv2.imshow(f"[{ID}] Receiving", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                print(f"[{ID}] Stopping application...")
                break

        except Exception as e:
            print(f"Error processing frame: {e}")
            continue
        
        except KeyboardInterrupt:
            print(f"[{ID}] Stopping application...")
            break

except Exception as e:
    print(f"Error in main loop: {e}")
    
finally:
    print(f"[{ID}] Cleaning up resources...")
    if udp_receiver is not None:
        udp_receiver.stop_recv_thread()
        time.sleep(0.5)
    
    print(f"[{ID}] Closing OpenCV windows...")
    cv2.destroyAllWindows()
    time.sleep(0.2)
    print(f"[{ID}] Application terminated successfully")
