from isaacsim import SimulationApp

# Boot Isaac Sim in headless mode
simulation_app = SimulationApp({"headless": True})

import omni
from omni.isaac.core.utils.extensions import enable_extension
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.core import World

# 1. Enable WebRTC Streaming for Browser Viewer
print("Enabling WebRTC Stream...")
enable_extension("omni.services.streamclient.webrtc")

# 2. Setup the World
print("Setting up the world...")
world = World()

# Spawn a simple cube for testing
from omni.isaac.core.objects import DynamicCuboid
import numpy as np

cube = DynamicCuboid(
    prim_path="/World/Cube",
    name="cube",
    position=np.array([0.0, 0.0, 1.0]),
    scale=np.array([1.0, 1.0, 1.0]),
    color=np.array([1.0, 0.0, 0.0])
)
world.scene.add(cube)

# Reset world to start physics
world.reset()

# Point the default camera at the cube
set_camera_view(eye=np.array([5.0, 5.0, 5.0]), target=np.array([0.0, 0.0, 0.0]))

print("==================================================")
print("Isaac Sim is running!")
print("To view the stream, open a browser on your local PC and go to:")
print("http://localhost:8211/streaming/webrtc-client/")
print("(Make sure you have forwarded port 8211 in your IDE!)")
print("==================================================")

# 3. Main Simulation Loop
while simulation_app.is_running():
    world.step(render=True)

# Cleanup
simulation_app.close()
