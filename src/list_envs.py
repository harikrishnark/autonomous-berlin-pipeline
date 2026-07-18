from isaacsim import SimulationApp
app = SimulationApp({"headless": True})
import omni.client
from omni.isaac.core.utils.nucleus import get_assets_root_path

def list_environments():
    root = get_assets_root_path()
    if not root:
        print("No nucleus server found")
        return
    print(f"Nucleus root: {root}")
    result, entries = omni.client.list(root + "/Isaac/Environments")
    for e in entries:
        print(e.relative_path)

list_environments()
app.close()
