from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

print("\n--- Inspecting omni.isaac.core ---")
try:
    import omni.isaac.core as oic
    print("omni.isaac.core found! Attributes:")
    print([x for x in dir(oic) if not x.startswith("_")])
except Exception as e:
    print("Failed to import omni.isaac.core:", e)

print("\n--- Inspecting isaacsim.core ---")
try:
    import isaacsim.core as ic
    print("isaacsim.core found! Attributes:")
    print([x for x in dir(ic) if not x.startswith("_")])
except Exception as e:
    print("Failed to import isaacsim.core:", e)

print("\n--- Checking World specifically ---")
try:
    from omni.isaac.core import World
    print("Successfully imported World from omni.isaac.core!")
except Exception as e:
    print("Failed from omni.isaac.core:", e)

try:
    from isaacsim.core import World
    print("Successfully imported World from isaacsim.core!")
except Exception as e:
    print("Failed from isaacsim.core:", e)

app.close()
