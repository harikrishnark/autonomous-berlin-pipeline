import argparse
import sys
import socket
import struct
import cv2
import numpy as np

# Start the Isaac Sim application before importing any core modules
from isaacsim import SimulationApp

parser = argparse.ArgumentParser(description="Create Urban Construction Scene")
parser.add_argument("--headless", action="store_true", help="Run in headless mode")
args = parser.parse_args()

config = {"headless": args.headless}
simulation_app = SimulationApp(config)

import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from pxr import UsdGeom, Gf

# For robot and camera
from omni.isaac.core.articulations import Articulation
from omni.isaac.sensor import Camera

def create_scene():
    world = World(stage_units_in_meters=1.0)

    # Base Paths for NVIDIA Isaac Sim Assets
    from isaacsim.storage.native import get_assets_root_path
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        print("Could not find Isaac Sim assets folder")
        simulation_app.close()
        sys.exit()

    print(f"Assets root path: {assets_root_path}")
    stage = omni.usd.get_context().get_stage()

    def set_translation(prim_path, pos):
        prim = stage.GetPrimAtPath(prim_path)
        xform = UsdGeom.XformCommonAPI(prim)
        xform.SetTranslate(Gf.Vec3d(float(pos[0]), float(pos[1]), float(pos[2])))

    # 1. Spawn a full environment
    env_asset = assets_root_path + "/Isaac/Environments/Simple_Warehouse/warehouse.usd"
    env_path = "/World/Environment"
    add_reference_to_stage(usd_path=env_asset, prim_path=env_path)
    print("Added full environment")

    # 2. Spawn Traffic Cones
    cone_asset = assets_root_path + "/Isaac/Environments/Simple_Warehouse/Props/S_TrafficCone.usd"
    for i in range(5):
        cone_path = f"/World/Construction/Cone_{i}"
        add_reference_to_stage(usd_path=cone_asset, prim_path=cone_path)
        set_translation(cone_path, [i * 1.5, 2.0, 0.0])
        print(f"Added cone {i}")

    # 3. Spawn a Pedestrian
    pedestrian_asset = assets_root_path + "/Isaac/People/Characters/original_male_adult_construction_01/male_adult_construction_01.usd"
    pedestrian_path = "/World/Pedestrians/Pedestrian_1"
    add_reference_to_stage(usd_path=pedestrian_asset, prim_path=pedestrian_path)
    set_translation(pedestrian_path, [2.0, 0.0, 0.0])

    # 4. Spawn an Autonomous Vehicle (Carter)
    vehicle_asset = assets_root_path + "/Isaac/Robots/NVIDIA/Carter/carter_v1.usd"
    vehicle_path = "/World/Vehicle/Carter"
    add_reference_to_stage(usd_path=vehicle_asset, prim_path=vehicle_path)
    set_translation(vehicle_path, [-3.0, 0.0, 0.0])
    
    carter = Articulation(prim_path=vehicle_path, name="carter")
    world.scene.add(carter)

    # 5. Add a Camera to Carter
    camera_path = "/World/Vehicle/Carter/chassis_link/Camera"
    camera = Camera(
        prim_path=camera_path,
        position=np.array([0.5, 0.0, 0.5]),
        frequency=20,
        resolution=(640, 480),
        orientation=np.array([0.5, -0.5, 0.5, -0.5]) # Looking forward
    )
    camera.initialize()
    
    print("Scene populated successfully.")
    
    # 6. Initialize Socket Connection to network_brain.py
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connected = False
    try:
        client_socket.connect(('127.0.0.1', 5005))
        print("✅ Connected to AI Brain!")
        socket_connected = True
    except Exception as e:
        print("⚠️ AI Brain not running (network_brain.py). Simulation will run without perception control.")

    world.reset()

    # Find wheel joints to apply velocity
    left_wheel_idx = carter.get_dof_index("left_wheel")
    right_wheel_idx = carter.get_dof_index("right_wheel")

    print("Simulation scene is ready! You can now explore it in the GUI.")
    print("Press Ctrl+C in the terminal to exit, or close the window.")
    
    import os
    frames_dir = '/workspace/autonomous-berlin-pipeline/frames'
    os.makedirs(frames_dir, exist_ok=True)
    
    frame_count = 0
    max_frames = 200
    
    while frame_count < max_frames:
        world.step(render=True)
        frame_count += 1
        
        target_vel = 2.0
        response = "DRIVE"
        
        if socket_connected:
            pass # We fetch frame below regardless

        # Capture image from camera
        try:
            img_data = camera.get_rgba()
            if img_data is not None and img_data.shape[0] > 0:
                # Convert RGBA to RGB
                frame = img_data[:, :, :3].astype(np.uint8)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                if socket_connected:
                    try:
                        # Compress and send
                        _, encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                        data = encoded.tobytes()
                        client_socket.sendall(struct.pack('<I', len(data)))
                        client_socket.sendall(data)
                        
                        # Receive response
                        response = client_socket.recv(1024).decode('utf-8')
                        if response == "BRAKE":
                            target_vel = 0.0
                    except Exception as e:
                        print(f"Socket error: {e}")
                        socket_connected = False
                        
                # Add Text Overlay & Write to Video
                color = (0, 0, 255) if response == "BRAKE" else (0, 255, 0)
                if not socket_connected:
                    response = "NO AI"
                    color = (128, 128, 128)
                frame = cv2.resize(frame, (640, 480))
                cv2.putText(frame, f"AI Command: {response}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                
                # Write raw JPEG
                cv2.imwrite(os.path.join(frames_dir, f"frame_{frame_count:04d}.jpg"), frame)
            else:
                print("Warning: camera.get_rgba() returned empty or None data.")
        except Exception as e:
            import traceback
            print(f"Camera/Video error at frame {frame_count}: {e}")
            traceback.print_exc()
                
        # Apply velocity to wheels
        if left_wheel_idx is not None and right_wheel_idx is not None:
            carter.set_joint_velocities([target_vel, target_vel], joint_indices=[left_wheel_idx, right_wheel_idx])

    print("Simulation finished. Saved raw frames to", frames_dir)

if __name__ == "__main__":
    create_scene()
    simulation_app.close()
