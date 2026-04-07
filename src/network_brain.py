import socket
import struct
import cv2
import numpy as np
from ultralytics import YOLO

def start_server(host='0.0.0.0', port=5005):
    print("Loading PyTorch YOLOv8 model...")
    model = YOLO("yolov8n.pt")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"Waiting for CARLA teammate to connect to {host}:{port}...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"✅ CARLA Simulator connected from: {addr}")
        
        try:
            while True:
                # 1. Receive the size of the incoming image frame (4 bytes = unsigned int)
                length_data = conn.recv(4)
                if not length_data:
                    break
                    
                frame_length = struct.unpack('<I', length_data)[0]
                
                # 2. Receive the actual image frame bytes
                frame_data = b''
                while len(frame_data) < frame_length:
                    packet = conn.recv(frame_length - len(frame_data))
                    if not packet:
                        break
                    frame_data += packet
                
                if not frame_data:
                    break
                    
                # 3. Decode the byte array into a visual cv2 image
                nparr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is not None:
                    # 4. Run PyTorch YOLOv8 perception
                    results = model(frame, verbose=False)
                    
                    # Determine response
                    response_command = "DRIVE"  # Default
                    closest_car_y = 0
                    
                    for r in results:
                        for box in r.boxes:
                            class_id = int(box.cls[0])
                            # If it's a car (id 2) or person (id 0)
                            if class_id == 2 or class_id == 0:
                                y2 = float(box.xyxy[0][3]) # bottom y-coordinate
                                if y2 > closest_car_y:
                                    closest_car_y = y2
                                    
                    # Very simple logic: if the object's bottom edge is very low in the frame,
                    # it means it is very close to our camera. Trigger BRAKE!
                    # Frame height is typically 600 or 720. Let's say if y2 > 400 it's close.
                    if closest_car_y > 400:
                        response_command = "BRAKE"
                        print(f"🚨 Obstacle close (Y: {closest_car_y})! Sending BRAKE command to CARLA.")
                    else:
                        print("🟢 Path clear. Sending DRIVE command.")
                        
                    # 5. Send command back to CARLA
                    conn.sendall(response_command.encode('utf-8'))
                    
        except ConnectionResetError:
            print("Connection to CARLA lost. Waiting for reconnect...")
        finally:
            conn.close()
            print("Client disconnected.")

if __name__ == "__main__":
    start_server()
