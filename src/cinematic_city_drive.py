import argparse
import sys
import os
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true", default=False)
args = parser.parse_args()

print("Initializing Isaac Sim Cinematic Drive...")
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": args.headless})

if args.headless:
    import carb
    carb.settings.get_settings().set("/app/livestream/port", 49100)
    import omni.kit.app
    ext_manager = omni.kit.app.get_app().get_extension_manager()
    ext_manager.set_extension_enabled_immediate("omni.services.streamclient.webrtc", True)

from omni.isaac.core import World
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.wheeled_robots.robots import WheeledRobot
from omni.isaac.sensor import Camera
from omni.isaac.core.utils.types import ArticulationAction

def create_scene():
    world = World(stage_units_in_meters=1.0)
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        print("ERROR: Nucleus server not found.")
        return

    # 1. Load Rivermark City Environment
    print("Loading Rivermark City...")
    city_asset_path = assets_root_path + "/Isaac/Environments/Outdoor/Rivermark/rivermark.usd"
    add_reference_to_stage(usd_path=city_asset_path, prim_path="/World/City")

    import omni
    from pxr import UsdGeom, Gf
    stage = omni.usd.get_context().get_stage()

    def set_translation(prim_path, pos):
        prim = stage.GetPrimAtPath(prim_path)
        xform = UsdGeom.XformCommonAPI(prim)
        xform.SetTranslate(Gf.Vec3d(float(pos[0]), float(pos[1]), float(pos[2])))

    # 2. Spawn the Vehicle (Carter v1)
    print("Spawning Vehicle...")
    carter_asset_path = assets_root_path + "/Isaac/Robots/NVIDIA/Carter/carter_v1.usd"
    vehicle_path = "/World/Vehicle/Carter"
    add_reference_to_stage(usd_path=carter_asset_path, prim_path=vehicle_path)
    set_translation(vehicle_path, [0.0, 0.0, 0.5])

    from omni.isaac.core.articulations import Articulation
    carter = Articulation(prim_path=vehicle_path, name="carter")
    world.scene.add(carter)

    # 3. Create Cinematic Drone Camera (Follow Cam)
    print("Initializing Cinematic Camera...")
    # Parented to chassis_link, placed 5 meters behind, 2.5 meters high
    # Pitch down 15 degrees: w=0.9914, y=0.1305 (Quaternion: w, x, y, z)
    # Note: carter_v1 chassis is just /chassis_link
    camera = Camera(
        prim_path="/World/Vehicle/Carter/chassis_link/CinematicCamera",
        position=np.array([-5.0, 0.0, 2.5]),
        frequency=20,
        resolution=(1280, 720),
        orientation=np.array([0.9914, 0.0, 0.1305, 0.0])
    )
    camera.initialize()

    world.reset()
    camera.initialize()

    # Get wheel joints to apply velocity
    left_wheel_idx = carter.get_dof_index("left_wheel")
    right_wheel_idx = carter.get_dof_index("right_wheel")

    frames_dir = '/workspace/autonomous-berlin-pipeline/frames_cinematic'
    os.makedirs(frames_dir, exist_ok=True)
    
    # Clear old frames
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))

    frame_count = 0
    max_frames = 300 # 15 seconds at 20fps

    print("Simulation started. Recording frames...")
    while frame_count < max_frames:
        world.step(render=True)
        
        # Apply constant forward velocity
        if left_wheel_idx is not None and right_wheel_idx is not None:
            carter.set_joint_velocities([8.0, 8.0], joint_indices=[left_wheel_idx, right_wheel_idx])

        try:
            img_data = camera.get_rgba()
            if img_data is not None and img_data.shape[0] > 0:
                # Convert RGBA to RGB
                img_rgb = img_data[:, :, :3].astype(np.uint8)
                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(frame_path, img_bgr)
            else:
                print(f"Warning: camera.get_rgba() returned empty at frame {frame_count}.")
        except Exception as e:
            print(f"Camera error at frame {frame_count}: {e}")

        frame_count += 1
        if frame_count % 50 == 0:
            print(f"Recorded {frame_count} / {max_frames} frames...")

    print(f"Simulation finished. Saved raw frames to {frames_dir}")

if __name__ == "__main__":
    create_scene()
    simulation_app.close()
