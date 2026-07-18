import argparse
import sys
import os

# Parse arguments first using parse_known_args so we don't crash on internal omniverse arguments!
parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true", default=True)
args, unknown = parser.parse_known_args()

print("Initializing Isaac Sim Procedural City Scene...")
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": args.headless})

# Enable WebRTC Livestreaming
from omni.isaac.core.utils.extensions import enable_extension
enable_extension("omni.services.streamclient.webrtc")

# ALL OTHER IMPORTS MUST HAPPEN AFTER SimulationApp IS INITIALIZED!
import cv2
import numpy as np

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid, VisualCylinder
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.sensor import Camera
from pxr import Gf, UsdLux, UsdShade
from omni.isaac.core.prims import XFormPrim
from omni.isaac.core.utils.rotations import euler_angles_to_quat

def create_material(stage, path, color):
    material = UsdShade.Material.Define(stage, path)
    shader = UsdShade.Shader.Define(stage, f"{path}/Shader")
    shader.CreateIdAttr("PreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.8)
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    return material

from pxr import Sdf

def bind_material(prim, material):
    binding_api = UsdShade.MaterialBindingAPI.Apply(prim)
    binding_api.Bind(material)

def create_scene():
    world = World(stage_units_in_meters=1.0)
    stage = world.stage
    assets_root_path = get_assets_root_path()
    
    # Create Materials
    mat_green = create_material(stage, "/World/Looks/Green", (0.1, 0.5, 0.1))
    mat_road = create_material(stage, "/World/Looks/Road", (0.2, 0.2, 0.2))
    mat_building = create_material(stage, "/World/Looks/Building", (0.6, 0.6, 0.7))
    mat_car1 = create_material(stage, "/World/Looks/CarRed", (0.8, 0.1, 0.1))
    mat_car2 = create_material(stage, "/World/Looks/CarBlue", (0.1, 0.1, 0.8))

    print("Building Procedural City Layout...")
    
    # Ground Plane
    world.scene.add_default_ground_plane()
    
    # Roads
    road1 = VisualCuboid(prim_path="/World/Road1", name="road1", position=np.array([0, 0, 0.01]), scale=np.array([100, 6, 0.05]))
    road2 = VisualCuboid(prim_path="/World/Road2", name="road2", position=np.array([0, 0, 0.01]), scale=np.array([6, 100, 0.05]))
    bind_material(road1.prim, mat_road)
    bind_material(road2.prim, mat_road)

    # Buildings
    buildings = [
        {"path": "/World/Building1", "pos": [15, 15, 5], "scale": [12, 12, 10]},
        {"path": "/World/Building2", "pos": [-15, 15, 8], "scale": [15, 10, 16]},
        {"path": "/World/Building3", "pos": [15, -15, 6], "scale": [10, 15, 12]},
        {"path": "/World/Building4", "pos": [-15, -15, 4], "scale": [12, 12, 8]},
        {"path": "/World/Building5", "pos": [30, 30, 10], "scale": [10, 10, 20]},
        {"path": "/World/Building6", "pos": [-30, -30, 12], "scale": [15, 15, 24]},
    ]
    
    for idx, b in enumerate(buildings):
        b_prim = VisualCuboid(
            prim_path=b["path"],
            name=f"building_{idx}",
            position=np.array(b["pos"]),
            scale=np.array(b["scale"])
        )
        bind_material(b_prim.prim, mat_building)

    # Lighting
    print("Adding Lighting...")
    light = UsdLux.DomeLight.Define(world.stage, "/World/Light")
    light.CreateIntensityAttr(20.0)
    
    distant_light = UsdLux.DistantLight.Define(world.stage, "/World/SunLight")
    distant_light.CreateIntensityAttr(30.0)
    distant_light.CreateAngleAttr(0.5)
    distant_light.AddOrientOp().Set(Gf.Quatf(0.866, 0.0, 0.5, 0.0))
    
    # Spawn Cars
    print("Spawning Vehicles...")
    car_asset_path = assets_root_path + "/Isaac/Props/Traffic/Cars/sedan_car.usd"
    
    lanes = [
        {"name": "Eastbound", "start": [-40.0, -1.5, 0.1], "dir": [1.0, 0.0, 0.0], "yaw": 0.0, "mat": mat_car1},
        {"name": "Westbound", "start": [40.0, 1.5, 0.1], "dir": [-1.0, 0.0, 0.0], "yaw": 180.0, "mat": mat_car2},
        {"name": "Northbound", "start": [1.5, -40.0, 0.1], "dir": [0.0, 1.0, 0.0], "yaw": 90.0, "mat": mat_car1},
        {"name": "Southbound", "start": [-1.5, 40.0, 0.1], "dir": [0.0, -1.0, 0.0], "yaw": -90.0, "mat": mat_car2},
    ]

    vehicles = []
    for idx, lane in enumerate(lanes):
        vehicle_path = f"/World/Vehicle/Sedan_{idx}"
        add_reference_to_stage(usd_path=car_asset_path, prim_path=vehicle_path)
        quat = euler_angles_to_quat(np.array([0, 0, lane["yaw"]]), degrees=True)
        car = XFormPrim(
            prim_path=vehicle_path, 
            name=f"sedan_prim_{idx}", 
            position=np.array(lane["start"]), 
            orientation=quat
        )
        bind_material(car.prim, lane["mat"])
        vehicles.append({
            "prim": car,
            "pos": np.array(lane["start"]),
            "dir": np.array(lane["dir"]),
            "start": np.array(lane["start"])
        })

    # Setup Camera
    print("Initializing Camera...")
    camera = Camera(
        prim_path="/World/CinematicCamera",
        position=np.array([0, 0, 25]),
        frequency=30,
        resolution=(1280, 720),
        orientation=np.array([1.0, 0.0, 0.0, 0.0])
    )
    
    world.reset()
    camera.initialize()
    
    print("Warming up simulation to load assets and shaders...")
    for _ in range(300):
        world.step(render=True)

    frames_dir = '/workspace/autonomous-berlin-pipeline/frames_small_city'
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))

    print("Simulation started. Recording frames...")
    
    max_frames = 450 # 15 seconds at 30 fps
    velocity = 8.0 # m/s
    dt = 1.0 / 30.0
    
    for frame_count in range(max_frames):
        world.step(render=True)
        
        for v in vehicles:
            v["pos"] += v["dir"] * velocity * dt
            if np.abs(v["pos"][0]) > 45.0 or np.abs(v["pos"][1]) > 45.0:
                v["pos"] = np.copy(v["start"])
            v["prim"].set_world_pose(position=v["pos"])

        try:
            img_data = camera.get_rgba()
            if img_data is not None and img_data.shape[0] > 0:
                img_rgb = img_data[:, :, :3].astype(np.uint8)
                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(frame_path, img_bgr)
        except Exception as e:
            print(f"Exception at frame {frame_count}: {e}")

    print(f"Simulation finished. Saved {max_frames} raw frames to {frames_dir}")

if __name__ == "__main__":
    create_scene()
    simulation_app.close()
