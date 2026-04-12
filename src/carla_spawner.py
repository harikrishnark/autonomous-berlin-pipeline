import socket
import struct
import time
import numpy as np
import cv2  # Added for video recording
try:
    import carla
except ImportError:
    print("Warning: CARLA library not found. Ensure you are running this on the RunPod instance with CARLA installed.")

def process_image(image, client_socket, video_writer=None):
    """
    This function is called every time the CARLA camera captures a frame.
    It compresses the image and streams it over the network to Teammate A's Mac.
    """
    try:
        # Convert raw CARLA image data into a numpy array
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]  # Remove alpha channel

        # Encode and compress using OpenCV
        _, encoded_frame = cv2.imencode('.jpg', array, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        frame_data = encoded_frame.tobytes()

        # Save to MP4 Video
        if video_writer is not None:
            video_writer.write(array)

        # Send over TCP Socket
        client_socket.sendall(struct.pack('<I', len(frame_data)))
        client_socket.sendall(frame_data)
        
        # Wait for AI Brain's response
        response = client_socket.recv(1024).decode('utf-8')
        
        if response == "BRAKE":
            print("🚨 Received BRAKE signal from Mac! Applying max brakes...")
            # Here Teammate B will apply carla.VehicleControl(brake=1.0)
        else:
            print("🟢 Path Clear. Cruising...")
            # Here Teammate B will apply carla.VehicleControl(throttle=0.5)

    except Exception as e:
        print(f"Network error: {e}")

def main():
    # --- 1. CONNECT TO TEAMMATE A's MAC ---
    # Change this IP to the public IP of Teammate A's Mac/Router
    MAC_IP = '127.0.0.1' 
    MAC_PORT = 5005
    
    print(f"Connecting to AI Brain at {MAC_IP}:{MAC_PORT}...")
    ai_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ai_socket.connect((MAC_IP, MAC_PORT))
    except ConnectionRefusedError:
        print("❌ Could not connect to AI Brain. Make sure Teammate A is running network_brain.py!")
        return

    # --- 2. CONNECT TO CARLA SERVER ---
    print("Connecting to CARLA Simulator...")
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    # --- 3. SPAWN THE VEHICLE ---
    print("Spawning a Vehicle...")
    vehicle_bp = blueprint_library.filter('model3')[0] # Spawn a Tesla Model 3
    spawn_point = world.get_map().get_spawn_points()[0]
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    
    # Put vehicle in autopilot for now so it moves
    vehicle.set_autopilot(True)

    # --- 4. ATTACH THE CAMERA ---
    print("Attaching RGB Camera...")
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '640')
    camera_bp.set_attribute('image_size_y', '480')
    camera_bp.set_attribute('fov', '110')
    
    # Mount camera on the hood
    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

    # --- 5. SETUP VIDEO RECORDING ---
    print("Initializing MP4 Video Recorder...")
    # 20 FPS is standard for CARLA camera listeners
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('simulation_run.mp4', fourcc, 20.0, (640, 480))

    # --- 6. START STREAMING ---
    # Every time the camera takes a photo, trigger `process_image`
    camera.listen(lambda image: process_image(image, ai_socket, video_writer))

    print("Simulation running. Streaming data to Mac. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Saving MP4 video and destroying actors...")
        video_writer.release()
        camera.destroy()
        vehicle.destroy()
        ai_socket.close()

if __name__ == '__main__':
    main()
