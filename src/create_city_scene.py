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
from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid
from omni.isaac.core.utils.stage import add_reference_to_stage, save_stage
from omni.isaac.core.utils.prims import create_prim
import numpy as np

def create_scene():
    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()

    # Base Paths for NVIDIA Isaac Sim Assets
    NUCLEUS_SERVER = "omniverse://localhost/NVIDIA/Assets/Isaac/4.0" # Fallback/generic path format
    
    # In Isaac Sim 6.0, assets are typically on the nucleus server. 
    # For a standalone script that runs locally, we can use the get_assets_root_path utility
    from omni.isaac.core.utils.nucleus import get_assets_root_path
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        print("Could not find Isaac Sim assets folder")
        simulation_app.close()
        sys.exit()

    print(f"Assets root path: {assets_root_path}")

    # 1. Spawn a basic road / ground (using a generic grid for now if City isn't immediately available)
    # 2. Spawn Traffic Cones (SimReady)
    cone_asset = assets_root_path + "/Isaac/Environments/Simple_Room/Props/traffic_cone.usd"
    
    for i in range(5):
        cone_path = f"/World/Construction/Cone_{i}"
        add_reference_to_stage(usd_path=cone_asset, prim_path=cone_path)
        # Position cones in a line
        create_prim(cone_path, translation=np.array([i * 1.5, 2.0, 0.0]))
        print(f"Added cone {i}")

    # 3. Spawn a Barricade
    barricade_asset = assets_root_path + "/Isaac/Environments/Simple_Room/Props/barrier.usd"
    barricade_path = "/World/Construction/Barricade"
    add_reference_to_stage(usd_path=barricade_asset, prim_path=barricade_path)
    create_prim(barricade_path, translation=np.array([3.0, 3.0, 0.0]))
    
    # 4. Spawn a Pedestrian
    # We will use a standard human asset
    pedestrian_asset = assets_root_path + "/Isaac/People/Characters/original_male_adult_police_03/original_male_adult_police_03.usd"
    pedestrian_path = "/World/Pedestrians/Pedestrian_1"
    add_reference_to_stage(usd_path=pedestrian_asset, prim_path=pedestrian_path)
    create_prim(pedestrian_path, translation=np.array([0.0, -2.0, 0.0]))

    # 5. Spawn an Autonomous Vehicle
    vehicle_asset = assets_root_path + "/Isaac/Robots/Carter/carter_v1.usd"
    vehicle_path = "/World/Vehicle/Carter"
    add_reference_to_stage(usd_path=vehicle_asset, prim_path=vehicle_path)
    create_prim(vehicle_path, translation=np.array([-3.0, 0.0, 0.0]))

    print("Scene populated successfully.")
    
    # Save the USD file locally so it can be opened easily
    usd_save_path = "/workspace/autonomous-berlin-pipeline/urban_construction_scene.usd"
    save_stage(usd_save_path)
    print(f"Scene saved to: {usd_save_path}")

    world.reset()
    
    print("Simulation scene is ready! You can now explore it in the GUI.")
    print("Press Ctrl+C in the terminal to exit, or close the window.")
    while simulation_app.is_running():
        world.step(render=True)

if __name__ == "__main__":
    create_scene()
    simulation_app.close()
