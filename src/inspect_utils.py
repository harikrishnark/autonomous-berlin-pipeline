from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

print("\n--- Checking utils imports ---")
try:
    from isaacsim.core.utils.stage import add_reference_to_stage, save_stage
    print("Successfully imported stage utils!")
except Exception as e:
    print("Failed to import stage utils:", e)

try:
    from isaacsim.core.utils.prims import create_prim
    print("Successfully imported create_prim!")
except Exception as e:
    print("Failed to import create_prim:", e)

try:
    from isaacsim.core.utils.nucleus import get_assets_root_path
    print("Successfully imported get_assets_root_path!")
except Exception as e:
    print("Failed to import get_assets_root_path:", e)

app.close()
