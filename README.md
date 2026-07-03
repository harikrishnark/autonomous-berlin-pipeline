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

The current shared simulation VM is a RunPod PyTorch instance for Isaac Sim work.

- SSH endpoint: `ssh root@157.157.221.29 -p 25388 -i ~/.ssh/id_ed25519`
- SSH proxy endpoint: `ssh ntu0wjwdd0eb2p-644117ed@ssh.runpod.io -i ~/.ssh/id_ed25519`
- Web terminal: Port 19123 via the exposed RunPod proxied URL

1. Connect to the VM using the SSH command above.
2. Clone this project under `~/autonomous-berlin-pipeline/`.
3. Keep the Jupyter and streaming ports restricted to trusted access.

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

## Current Progress (2026-07-03)

The shared Isaac Sim VM is reachable and the simulator runtime is functioning. A remote benchmark run completed successfully and reported a mean FPS of about 20.05 with the app startup sequence finishing normally.

What is verified so far:
- SSH access to the RunPod VM is working.
- The Isaac Sim benchmark workflow completed remotely and produced benchmark metrics.
- The remote shell reached the simulation startup and shutdown phases without a GPU/runtime crash.

What is still pending:
- A confirmed local download of the benchmark artifact files from the VM.
- A working WebRTC/livestream export path for a real Isaac Sim video stream.
- A decision on whether to continue troubleshooting the live stream or keep using the local fallback video generation path for the demo.

Needed details to continue the conversation:
- Preferred output artifact: benchmark report, image sequence, MP4, or live stream.
- Preferred delivery method: direct download from the VM or browser-based streaming.
- Whether the team wants to prioritize stream stability or move forward with the fallback demo path.

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
