from isaacsim import SimulationApp
import sys

# Start the simulation app in headless mode
app = SimulationApp({"headless": True})

ext_manager = app.app.get_extension_manager()
exts = ext_manager.get_extensions()

print("Listing all extensions related to 'stream' or 'live':")
found = False
for ext in exts:
    ext_id = ext.get("id", "")
    if "stream" in ext_id or "live" in ext_id:
        print(f" - {ext_id}")
        found = True

if not found:
    print("No stream or live extensions found.")

app.close()
