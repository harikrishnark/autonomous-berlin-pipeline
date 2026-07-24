import cv2
import numpy as np

print("Initializing SimulationApp...")
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid
from pxr import UsdLux
import omni.replicator.core as rep

world = World(stage_units_in_meters=1.0)

# Add Dome Light
light = UsdLux.DomeLight.Define(world.stage, "/World/Light")
light.CreateIntensityAttr(3000.0)

# Add Green Cube at origin
cube = VisualCuboid(
    prim_path="/World/Cube",
    name="cube",
    position=np.array([0.0, 0.0, 1.0]),
    scale=np.array([2.0, 2.0, 2.0]),
    color=np.array([0.0, 1.0, 0.0])
)

# Use replicator to create camera
camera = rep.create.camera(position=(0, 0, 45), look_at=(0, 0, 0))
render_product = rep.create.render_product(camera, (1280, 720))
rgb_annot = rep.AnnotatorRegistry.get_annotator("rgb")
rgb_annot.attach(render_product)

world.reset()

print("Warming up...")
for _ in range(60):
    world.step(render=True)
    rep.orchestrator.step()

img_data = rgb_annot.get_data()
if img_data is not None and img_data.shape[0] > 0:
    print(f"Image shape: {img_data.shape}, min: {img_data.min()}, max: {img_data.max()}, mean: {img_data.mean()}")
    img_bgr = cv2.cvtColor(img_data[:, :, :3], cv2.COLOR_RGB2BGR)
    cv2.imwrite("test_rep_output.jpg", img_bgr)
    print("Saved test_rep_output.jpg")
else:
    print("Image is None or empty!")

simulation_app.close()
