# City Demo — How to Use

`simple_city_car.py` renders a 10-second orbit video of a car (NVIDIA Leatherback) parked on a street in the Rivermark city environment, using Isaac Sim headless. Output: [simple_city_car.mp4](simple_city_car.mp4).

## Requirements

- **Isaac Sim 5.1** installed via pip in a Python 3.11 venv (`pip install isaacsim[all]==5.1.0.0 --extra-index-url https://pypi.nvidia.com`)
- NVIDIA GPU with RT cores, 16 GB+ VRAM, driver 550+ (tested on RTX 4000 Ada / RunPod)
- Ubuntu 22.04

## Setup (run after every pod restart)

System packages don't persist across RunPod container restarts — reinstall them each time:

```bash
apt-get update && apt-get install -y xvfb ffmpeg libglu1-mesa libegl1
```

> **Why `libglu1-mesa` matters:** without it, Isaac Sim starts fine but the RTX
> material system (MDL/neuray) fails to load, every shader build fails, and the
> camera silently returns empty frames. No crash, no obvious error — just a
> black/empty render. This cost us a full render cycle to diagnose.

## Run

```bash
export OMNI_KIT_ACCEPT_EULA=yes
xvfb-run -a -s "-screen 0 1280x720x24" python -u simple_city_car.py
ffmpeg -framerate 20 -i simple_city_frames/frame_%04d.jpg \
       -c:v libx264 -pix_fmt yuv420p simple_city_car.mp4
```

First run takes longer: Isaac Sim downloads its Kit extensions (~5 min) and streams the Rivermark environment from NVIDIA's asset CDN. Subsequent runs use the local cache.

## How the script works

1. `SimulationApp({"headless": True})` boots Isaac Sim without a GUI (must be the first Isaac import).
2. `add_reference_to_stage` loads the Rivermark city USD and the car USD into the stage.
3. The car is placed with `XFormPrim.set_world_pose` — **not** `XformCommonAPI`, which silently no-ops on prims that already have transform stacks.
4. The car is scaled 0.05× because the Leatherback USD is authored in centimeters (a raw load is ~40 m long). The script prints the car's bounding box so unit problems are caught immediately.
5. A `Camera` sensor orbits the car: per frame, its position moves along a circle and its orientation is recomputed to look at the car (yaw/pitch from the direction vector, converted to a quaternion).
6. The loop calls `world.render()` only — no physics stepping — then `camera.get_rgba()` grabs the frame as a numpy array, saved as JPEG via OpenCV.

## Hard-won debugging rules

- **Verify asset paths against the S3 bucket before coding.** `add_reference_to_stage` does not error on nonexistent URLs — the prim just stays empty. (The old `sedan_car.usd` path used elsewhere in this repo does not exist in the 5.1 asset tree.)
- **Print bounding boxes after loading assets** — catches both missing assets (empty bbox) and unit mismatches (bbox 100× too big).
- **Smoke-test with stills before a full render.** A 5-minute single-frame test catches framing, lighting, and placement bugs that would waste a 15-minute render.
- **Add lights.** Outdoor environments can render very dark headless; a `DistantLight` + `DomeLight` fixes exposure.
