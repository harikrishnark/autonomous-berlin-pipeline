from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

print("\n--- Inspecting isaacsim.core.api ---")
try:
    import isaacsim.core.api as ica
    print("isaacsim.core.api attributes:")
    print([x for x in dir(ica) if not x.startswith("_")])
except Exception as e:
    print("Failed to import isaacsim.core.api:", e)

print("\n--- Checking specific imports ---")
try:
    from isaacsim.core.api import World
    print("Successfully imported World from isaacsim.core.api!")
except Exception as e:
    print("Failed to import World:", e)

try:
    from isaacsim.core.api.objects import DynamicCuboid
    print("Successfully imported DynamicCuboid from isaacsim.core.api.objects!")
except Exception as e:
    print("Failed to import DynamicCuboid:", e)

try:
    from isaacsim.core.api.utils.stage import add_reference_to_stage
    print("Successfully imported add_reference_to_stage!")
except Exception as e:
    print("Failed to import add_reference_to_stage:", e)

app.close()
