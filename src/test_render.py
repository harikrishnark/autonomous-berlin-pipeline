import cv2
import numpy as np

print("Initializing SimulationApp...")
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid
from omni.isaac.sensor import Camera
from pxr import UsdLux
import omni.isaac.core.utils.rotations as rot_utils

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# Add Dome Light
light = UsdLux.DomeLight.Define(world.stage, "/World/Light")
light.CreateIntensityAttr(2000)

# Add Green Cube at origin
cube = VisualCuboid(
    prim_path="/World/Cube",
    name="cube",
    position=np.array([0.0, 0.0, 1.0]),
    scale=np.array([2.0, 2.0, 2.0]),
    color=np.array([0.0, 1.0, 0.0])
)

# Add Camera looking at origin from X=10, Y=0, Z=1
# Looking down -X axis
camera = Camera(
    prim_path="/World/TestCamera",
    position=np.array([0.0, 0.0, 45.0]),
    frequency=30,
    resolution=(1280, 720),
    orientation=np.array([1.0, 0.0, 0.0, 0.0])
)

world.reset()
camera.initialize()

print("Warming up...")
for _ in range(60):
    world.step(render=True)

img_data = camera.get_rgba()
if img_data is not None:
    print(f"Image shape: {img_data.shape}, min: {img_data.min()}, max: {img_data.max()}, mean: {img_data.mean()}")
else:
    print("Image is None!")

simulation_app.close()
