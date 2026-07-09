from isaacsim import SimulationApp

# Boot Isaac Sim in headless mode
simulation_app = SimulationApp({"headless": True})

import omni.kit.app
import time

# 1. Enable full streaming experience using the core extension manager
print("Enabling Full Streaming Experience (isaacsim.exp.full.streaming)...")
ext_manager = omni.kit.app.get_app().get_extension_manager()
ext_manager.set_extension_enabled_immediate("isaacsim.exp.full.streaming", True)

print("==================================================")
print("Isaac Sim is running!")
print("To view the stream over your VS Code SSH tunnel, check ports 8211 or 49100.")
print("==================================================")

# 2. Main Simulation Loop
while simulation_app.is_running():
    simulation_app.update()
    time.sleep(0.016)

# Cleanup
simulation_app.close()

