# Autonomous Berlin Pipeline

A hybrid autonomous driving software project designed to emulate the production and R&D toolchains used by major automotive manufacturers in Germany, with the final simulator direction set to **NVIDIA Isaac Sim / Omniverse** for cloud-hosted autonomy prototyping.

The goal is to build a portfolio-ready autonomy simulation pipeline: synthetic sensor data from Isaac Sim, Python perception, ROS 2 middleware, and C++ control logic.

> **Cloud-first:** All development and execution takes place on a shared GPU VM. The target simulator is **NVIDIA Isaac Sim 6.0.0** running headless in Docker with WebRTC streaming.

---

## System Architecture

The project is broken into three core layers:

1. **The Brain: Perception & AI**
   - **Stack:** Python, PyTorch, OpenCV, YOLOv8
   - **Function:** Processes camera/lidar-style sensor data to detect lanes, pedestrians, vehicles, and hazards.

2. **The Nervous System: Middleware**
   - **Stack:** ROS 2
   - **Function:** Broadcasts perception data such as bounding boxes, object class, confidence, and estimated distance so control logic can consume it.

3. **The Muscle: Vehicle Control**
   - **Stack:** Modern C++ using C++14/17
   - **Function:** Safe control logic that subscribes to ROS 2 topics. When the AI detects a hazard, the C++ node triggers a response such as emergency braking.

---

## Cloud Environment

All development is performed on a shared GPU VM. Both teammates SSH into the same remote machine so the simulator, perception process, ROS 2 middleware, and control logic run in one reproducible environment.

**Initial budget:** $25 USD in cloud credits.

### Connecting to the VM

1. Log in to the selected GPU provider.
2. Start the shared GPU VM.
3. Connect with SSH or the provider web terminal.
4. Clone this project under `~/autonomous-berlin-pipeline/`.

### First-Time VM Setup

```bash
git clone https://github.com/harikrishnark/autonomous-berlin-pipeline.git
cd autonomous-berlin-pipeline

python3 -m venv venv
source venv/bin/activate

pip install ultralytics opencv-python torch

python src/brain_perception.py
```

See [implementation.md](./implementation.md) for the phased implementation plan.
See [docs/isaac_sim_deployment.md](./docs/isaac_sim_deployment.md) for the finalized Isaac Sim VM deployment plan.

---

## Repository Structure

```text
autonomous-berlin-pipeline/
├── src/
│   ├── brain_perception.py      # YOLOv8 inference and bounding box extraction
│   ├── network_brain.py         # Socket listener for simulator camera stream
│   ├── nvidia_simulator.py      # NVIDIA Isaac Sim integration scaffold
│   ├── mock_carla_client.py     # Local mock client for testing without full simulator
│   └── map_loader.py            # Map-loading helpers
├── data/                        # Git-ignored raw images, datasets, output videos
├── docs/isaac_sim_deployment.md # Final Isaac Sim VM deployment plan
├── TODO.md                      # Granular task checklist
├── implementation.md            # Base implementation plan
└── README.md
```

---

## Portfolio Positioning

This project should be presented as:

> A cloud-deployed NVIDIA Isaac Sim autonomy pipeline with ROS 2, synthetic sensor streams, YOLO-based perception, and a control loop that demonstrates hazard detection and braking in simulation.

This is intentionally scoped as a credible autonomy prototype, not a claim of production-level autonomous vehicle validation.
