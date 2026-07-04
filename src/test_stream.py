from isaacsim import SimulationApp

# Boot Isaac Sim in headless mode
simulation_app = SimulationApp({"headless": True})

import omni.kit.app
import time

# 1. Enable WebSocket Streaming for Browser Viewer using the core extension manager
print("Enabling WebSocket Stream (TCP Mode)...")
ext_manager = omni.kit.app.get_app().get_extension_manager()
ext_manager.set_extension_enabled_immediate("omni.services.streamclient.websocket", True)

print("==================================================")
print("Isaac Sim is running!")
print("To view the stream over your VS Code SSH tunnel, go to:")
print("http://localhost:8211/streaming/client/")
print("(Make sure you have forwarded both ports 8211 AND 8844 in your IDE!)")
print("==================================================")

# 2. Main Simulation Loop
while simulation_app.is_running():
    simulation_app.update()
    time.sleep(0.016)

# Cleanup
simulation_app.close()

