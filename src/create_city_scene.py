import argparse
import sys

# Start the Isaac Sim application before importing any core modules
from isaacsim import SimulationApp

parser = argparse.ArgumentParser(description="Create Urban Construction Scene")
parser.add_argument("--headless", action="store_true", help="Run in headless mode")
args = parser.parse_args()

config = {"headless": args.headless}
simulation_app = SimulationApp(config)

import omni
from isaacsim.core.api import World
from isaacsim.core.api.objects import DynamicCuboid
from isaacsim.core.utils.stage import add_reference_to_stage
import numpy as np
from pxr import UsdGeom, Gf

def create_scene():
    world = World(stage_units_in_meters=1.0)
    # Remove the generic ground plane, we will load a full environment
    # world.scene.add_default_ground_plane()

    # Base Paths for NVIDIA Isaac Sim Assets
    NUCLEUS_SERVER = "omniverse://localhost/NVIDIA/Assets/Isaac/4.0" # Fallback/generic path format
    
    # In Isaac Sim 6.0, assets are typically on the nucleus server. 
    # For a standalone script that runs locally, we can use the get_assets_root_path utility
    from isaacsim.storage.native import get_assets_root_path
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        print("Could not find Isaac Sim assets folder")
        simulation_app.close()
        sys.exit()

    print(f"Assets root path: {assets_root_path}")

    stage = omni.usd.get_context().get_stage()

    def set_translation(prim_path, pos):
        prim = stage.GetPrimAtPath(prim_path)
        xform = UsdGeom.XformCommonAPI(prim)
        xform.SetTranslate(Gf.Vec3d(float(pos[0]), float(pos[1]), float(pos[2])))

    # 1. Spawn a full environment
    env_asset = assets_root_path + "/Isaac/Environments/Simple_Warehouse/warehouse.usd"
    env_path = "/World/Environment"
    add_reference_to_stage(usd_path=env_asset, prim_path=env_path)
    print("Added full environment")

    # 2. Spawn Traffic Cones
    cone_asset = assets_root_path + "/Isaac/Environments/Simple_Warehouse/Props/S_TrafficCone.usd"
    for i in range(5):
        cone_path = f"/World/Construction/Cone_{i}"
        add_reference_to_stage(usd_path=cone_asset, prim_path=cone_path)
        set_translation(cone_path, [i * 1.5, 2.0, 0.0])
        print(f"Added cone {i}")

    # 3. Spawn a Barricade
    barricade_asset = assets_root_path + "/Isaac/SimReady/Industrial/Warehouse/Barriers/Barrier_Wall_Plastic_Orange_A03/sm_barrier_wall_plastic_orange_a03_01.usd"
    barricade_path = "/World/Construction/Barricade"
    add_reference_to_stage(usd_path=barricade_asset, prim_path=barricade_path)
    set_translation(barricade_path, [3.0, 3.0, 0.0])

    # 4. Spawn a Pedestrian
    pedestrian_asset = assets_root_path + "/Isaac/People/Characters/original_male_adult_construction_01/male_adult_construction_01.usd"
    pedestrian_path = "/World/Pedestrians/Pedestrian_1"
    add_reference_to_stage(usd_path=pedestrian_asset, prim_path=pedestrian_path)
    set_translation(pedestrian_path, [0.0, -2.0, 0.0])

    # 5. Spawn an Autonomous Vehicle
    vehicle_asset = assets_root_path + "/Isaac/Robots/NVIDIA/Carter/carter_v1.usd"
    vehicle_path = "/World/Vehicle/Carter"
    add_reference_to_stage(usd_path=vehicle_asset, prim_path=vehicle_path)
    set_translation(vehicle_path, [-3.0, 0.0, 0.0])

    print("Scene populated successfully.")
    
    # Save the USD file locally so it can be opened easily
    usd_save_path = "/workspace/autonomous-berlin-pipeline/urban_construction_scene.usd"
    stage.Export(usd_save_path)
    print(f"Scene saved to: {usd_save_path}")

    print("Simulation scene is ready! You can now explore it in the GUI.")
    print("Press Ctrl+C in the terminal to exit, or close the window.")
    while simulation_app.is_running():
        world.step(render=True)

if __name__ == "__main__":
    create_scene()
    simulation_app.close()
