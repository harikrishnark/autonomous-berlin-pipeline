# Project Handoff Summary: Autonomous Berlin Pipeline

## Overview
This document summarizes the current state, technical decisions, and future roadmap of the **Autonomous Berlin Pipeline**. It is designed to be fed directly into an AI assistant (like Gemini) to seamlessly resume development without losing context.

**Goal:** Build a cloud-deployed NVIDIA Isaac Sim autonomy pipeline with ROS 2, synthetic camera/lidar streams, YOLO-based perception, and a control loop that demonstrates hazard detection and braking in simulation.

---

## 1. What We Accomplished

### Infrastructure & Cloud Deployment
We heavily explored and tested deployment strategies on **RunPod** to host NVIDIA Isaac Sim headless. We encountered and diagnosed several critical cloud infrastructure roadblocks:
- **The "Isaac Sim Container" Trap:** We initially deployed the official `nvcr.io/nvidia/isaac-sim:6.0.0` container on RunPod. While the simulator ran successfully (we executed Python benchmarking and generated synthetic dataset MP4s), the container environment was extremely restricted.
  - **No Root Access:** The container forces the `isaac-sim` user, preventing us from running SSH daemons for IDE connections.
  - **Proxy Limitations:** RunPod's Web Terminal and Proxy SSH (`ssh.runpod.io`) block advanced IDE features (VS Code / Antigravity IDE) from connecting.
  - **WebRTC UDP Blocking:** Isaac Sim's native WebRTC video streaming failed because WebRTC media strictly requires UDP (port 47998), but the standard RunPod templates only map TCP ports. This resulted in a "black screen" when using the Isaac Sim WebRTC Streaming Client.

### The Strategic Pivot
To solve all networking and IDE integration issues, we pivoted to a **RunPod PyTorch 2.4.0 Template** with a persistent Network Volume mounted at `/workspace`.
- **Why this works:** The PyTorch template provides direct TCP SSH port mapping, full `root` access, and an unrestricted Ubuntu base. This allows VS Code (Remote - SSH) and the Antigravity IDE to connect programmatically and flawlessly. 
- **SSH Configured:** The local `~/.ssh/config` is configured with a `runpod` host pointing to the new PyTorch direct TCP endpoint.
- **Documentation Updated:** `README.md` and onboarding docs were updated with the new PyTorch SSH endpoints and pushed to the `main` branch.

### Synthetic Data Generation
Before migrating away from the Docker container, we successfully ran Isaac Sim's Replicator API (`offline_generation.py`) to procedurally generate synthetic datasets (RGB, Depth, Segmentation videos) and hosted them using a temporary Python HTTP server for local download.

---

## 2. The Current State of the Environment

- **Host:** RunPod Ubuntu (PyTorch 2.4.0 Template)
- **Directory:** `/workspace/autonomous-berlin-pipeline/` (Mounted on a persistent network volume).
- **IDE Access:** Working perfectly via VS Code / Antigravity IDE using the `runpod` SSH host.
- *Note:* There are some leftover files in `/workspace` owned by the previous `isaac-sim` user (UID 1000/1234) which cannot be easily deleted due to NFS root-squashing. New development should happen in fresh directories or by ignoring the locked files.

---

## 3. Next Steps & The Immediate Plan

The next AI assistant should pick up exactly from here. 

### Step A: Install Isaac Sim 6.0 Natively via PIP
Since we are on a generic PyTorch Ubuntu image, we need to install Isaac Sim natively. Isaac Sim 6.0 has a strict requirement for **Python 3.12** (which is newer than what PyTorch containers usually default to).
1. Connect via VS Code IDE.
2. Install Python 3.12: `apt update && apt install python3.12-venv -y`
3. Create an isolated environment: `python3.12 -m venv /workspace/isaac_env && source /workspace/isaac_env/bin/activate`
4. Install Isaac Sim: `pip install "isaacsim[all,extscache]==6.0.1" --extra-index-url https://pypi.nvidia.com`

### Step B: Build the Self-Driving Environment
Once Isaac Sim is installed, begin constructing the simulation:
1. **The Map:** Import OpenStreetMap (OSM) data or use pre-built Isaac Sim `City` environments to generate roads, traffic lights, and footpaths.
2. **Dynamic Actors:** Use the `omni.anim.people` extension to generate pedestrian crowds with realistic navmesh walking behaviors.
3. **The Vehicle:** Implement a Wheeled Robot controller in Python to command the autonomous vehicle to follow waypoints.

### Step C: Integrate the Pipeline (ROS 2 & YOLO)
1. Attach virtual cameras and LiDAR to the simulated vehicle.
2. Bridge the sensor data out of Isaac Sim using the **ROS 2 bridge**.
3. Use `src/brain_perception.py` (YOLOv8) to process the ROS 2 camera stream, detect hazards (pedestrians/cars), and send braking signals back to the simulator via C++ control nodes.

---
*End of Handoff Document.*
