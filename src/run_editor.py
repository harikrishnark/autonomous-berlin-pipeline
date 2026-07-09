from isaacsim import SimulationApp
import time

# Boot Isaac Sim in full GUI mode (headless=False)
# It will render to the virtual display (:1) where VNC is looking
print("Starting Isaac Sim in GUI mode on display :1...")
simulation_app = SimulationApp({"headless": False})

print("==================================================")
print("Isaac Sim Editor is now running in GUI mode!")
print("Connect via VNC on port 5900 to see and use the editor.")
print("==================================================")

# Loop to keep the app active and responsive
while simulation_app.is_running():
    simulation_app.update()
    time.sleep(0.016)

simulation_app.close()
