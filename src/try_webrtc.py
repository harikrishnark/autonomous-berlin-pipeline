from isaacsim import SimulationApp
import omni.kit.app

app = SimulationApp({"headless": True})
ext_manager = omni.kit.app.get_app().get_extension_manager()

print("Attempting to enable omni.services.streamclient.webrtc...")
try:
    success = ext_manager.set_extension_enabled_immediate("omni.services.streamclient.webrtc", True)
    print(f"Enable success: {success}")
except Exception as e:
    print(f"Error: {e}")

app.close()
