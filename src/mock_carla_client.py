import socket
import struct
import cv2
import time

def mock_carla_camera(host='127.0.0.0', port=5005):
    """
    Simulates the CARLA simulator by reading your Mac's webcam (or a video file)
    and streaming it to the network_brain.py server over TCP.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"Attempting to connect to AI Brain at {host}:{port}...")
    try:
        # Use 127.0.0.1 (localhost) since both scripts will run on your Mac for testing
        client_socket.connect(('127.0.0.1', port))
        print("✅ Connected to AI Brain!")
    except ConnectionRefusedError:
        print("❌ Could not connect! Make sure network_brain.py is running first.")
        return

    # Try webcam (0), but if macOS privacy settings block it, fall back to the static image!
    cap = cv2.VideoCapture(0)
    
    use_static_image = False
    
    if not cap.isOpened():
        print("⚠️ Warning: Could not open Mac webcam (likely blocked by macOS Privacy Settings).")
        print("Falling back to streaming the static 'bus.jpg' image to simulate continuous video feed...")
        use_static_image = True
        # Make sure bus.jpg exists, fallback to ultralytics download
        import os
        import urllib.request
        if not os.path.exists("bus.jpg"):
            urllib.request.urlretrieve("https://ultralytics.com/images/bus.jpg", "bus.jpg")

    try:
        while True:
            if use_static_image:
                frame = cv2.imread("bus.jpg")
                if frame is None:
                    print("Error: Could not load bus.jpg")
                    break
            else:
                ret, frame = cap.read()
                if not ret:
                    break
                
            # Resize frame to save bandwidth (like CARLA would)
            frame = cv2.resize(frame, (640, 480))

            # Encode frame to JPEG byte array
            _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame_data = encoded_frame.tobytes()
            
            # Send length of the frame first (4 bytes), then the actual frame
            client_socket.sendall(struct.pack('<I', len(frame_data)))
            client_socket.sendall(frame_data)
            
            # Wait for Brain's response (DRIVE or BRAKE)
            response = client_socket.recv(1024).decode('utf-8')
            
            # Display real-time output in the terminal
            if response == "BRAKE":
                print("🛑 AI says: BRAKE! (Obstacle detected near camera)")
            else:
                print("🟢 AI says: DRIVE")
                
            # Cap the framerate to roughly 15 FPS so we don't overload our local socket
            time.sleep(0.06)
            
    except Exception as e:
        print(f"Stream stopped: {e}")
    finally:
        cap.release()
        client_socket.close()

if __name__ == "__main__":
    mock_carla_camera()
