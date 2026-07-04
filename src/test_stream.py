from isaacsim import SimulationApp

# Boot Isaac Sim in headless mode
simulation_app = SimulationApp({"headless": True})

import omni.ext
import time

# 1. Enable WebRTC Streaming for Browser Viewer using the core extension manager
print("Enabling WebRTC Stream...")
ext_manager = omni.ext.get_extension_manager()
ext_manager.enable_extension("omni.services.streamclient.webrtc")

print("==================================================")
print("Isaac Sim is running!")
print("To view the stream, open a browser on your local PC and go to:")
print("http://localhost:8211/streaming/webrtc-client/")
print("(Make sure you have forwarded port 8211 in your IDE!)")
print("==================================================")

# 2. Main Simulation Loop
while simulation_app.is_running():
    simulation_app.update()
    time.sleep(0.016)

# Cleanup
simulation_app.close()

