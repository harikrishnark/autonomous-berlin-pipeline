# Autonomous Berlin Pipeline

A hybrid autonomous driving software project designed to emulate the production and R&D toolchains used by major automotive manufacturers in Germany (Volkswagen/CARIAD, BMW, Mercedes-Benz, and Tesla).

This project is a joint effort structured around a **"Divide and Conquer"** architecture, separating AI perception from lower-level safety algorithms to mimic real-world vehicle software layers.

> **☁️ Cloud-First:** All development and execution takes place on a shared remote VM (RunPod). We have **$25 in initial cloud credits**. Neither teammate runs code locally — the VM is the single source of truth for the simulation environment.

---

## 🏗 System Architecture

The project is broken into three core layers:

1. **The Brain (Perception & AI)**
   - **Stack:** Python, PyTorch, OpenCV, YOLOv8
   - **Function:** Processes raw camera/LiDAR data to detect lanes, pedestrians, vehicles, and calculate distance.

2. **The Nervous System (Middleware)**
   - **Stack:** ROS 2 (Robot Operating System)
   - **Function:** Broadcasts perception data (bounding boxes, object distance) from the Python node over the network so control logic can consume it with safety guarantees.

3. **The Muscle (Vehicle Control)**
   - **Stack:** Modern C++ (C++14/17)
   - **Function:** Safe, mathematical control logic (PID controllers) that subscribes to the ROS 2 node. When the AI detects a hazard, the C++ code triggers the appropriate vehicle response (e.g., emergency braking).

---

## ☁️ Cloud Environment

All development is performed on a shared **RunPod** GPU instance. Both teammates SSH into the same remote VM — there is no local development or split environment.

**Initial budget:** $25 USD in RunPod credits.

### Connecting to the VM
1. Log in to [RunPod](https://runpod.io) and navigate to the shared pod.
2. Use the provided SSH command or the RunPod web terminal.
3. The project is cloned under `~/autonomous-berlin-pipeline/`.

### First-Time VM Setup
```bash
# Clone the repo (only needed once)
git clone https://github.com/harikrishnark/autonomous-berlin-pipeline.git
cd autonomous-berlin-pipeline

# Create and activate Python environment
python3 -m venv venv
source venv/bin/activate

# Install perception dependencies
pip install ultralytics opencv-python torch

# Validate perception stack
python src/brain_perception.py
```

> See [`implementation.md`](./implementation.md) for the full phased implementation plan.

---

## 📁 Repository Structure

```
autonomous-berlin-pipeline/
├── src/
│   ├── brain_perception.py     # YOLOv8 inference & bounding box extraction
│   ├── network_brain.py        # Socket listener for CARLA camera stream
│   ├── carla_spawner.py        # Spawns vehicle + camera in CARLA, streams output
│   └── mock_carla_client.py    # Local mock client for testing without full CARLA
├── data/                       # (Git-ignored) Raw images, datasets, output videos
├── TODO.md                     # Granular task checklist
├── implementation.md           # Base implementation plan
└── README.md                   # This file
```
