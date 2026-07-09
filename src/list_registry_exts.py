from isaacsim import SimulationApp

app = SimulationApp({"headless": True})
ext_manager = app.app.get_extension_manager()

registry = ext_manager.get_registry()
print("Searching registry for 'stream' and 'webrtc'...")
# List versions of some extensions
for name in ["omni.services.streamclient.webrtc", "omni.services.streamclient.websocket", "omni.kit.livestream.webrtc"]:
    try:
        versions = ext_manager.get_registry_extension_versions(name)
        print(f"Versions for {name}: {versions}")
    except Exception as e:
        print(f"Error checking {name}: {e}")

app.close()
