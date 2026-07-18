# Task List: Distributed NVIDIA Isaac Sim Pipeline

## Current Status (2026-07-03)

- [x] Confirmed SSH access to the shared RunPod Isaac Sim VM.
- [x] Verified that the Isaac Sim benchmark workflow completed remotely and produced runtime metrics.
- [ ] Retrieve the generated benchmark artifacts locally for review.
- [ ] Resolve the livestream/WebRTC export path for a true Isaac Sim video stream.
- [ ] Decide whether to continue with the live stream path or keep using the local fallback video output for the portfolio demo.

## Phase 1: Environment & Foundational Scripts

- [x] Set up Python environment with PyTorch and YOLOv8.
- [x] Write base neural network validation script `src/brain_perception.py`.
- [x] Initialize GitHub repository and commit code.
- [x] Write networking socket listener `src/network_brain.py` to receive simulator camera images.
- [x] Write simulator scaffold `src/nvidia_simulator.py`.
- [x] Write mock simulator client `src/mock_carla_client.py`.

## Phase 2: NVIDIA Isaac Sim Integration

- [ ] Rent GPU VM with RTX-capable NVIDIA GPU support.
- [ ] Install Docker.
- [ ] Install NVIDIA Container Toolkit.
- [ ] Validate GPU passthrough with CUDA `nvidia-smi` container.
- [ ] Pull `nvcr.io/nvidia/isaac-sim:6.0.0`.
- [ ] Start Isaac Sim headless with WebRTC streaming.
- [ ] Open/restrict required streaming ports: `49100/tcp`, `47998/udp`, and optionally `8210/tcp`.
- [ ] Connect from Isaac Sim WebRTC client or browser viewer.
- [ ] Create first Isaac Sim scene with ego agent and camera.
- [ ] Record first simulator output video.

## Phase 3: Perception-Control Fusion

- [ ] Connect `network_brain.py` to live Isaac Sim camera frames.
- [ ] Run YOLOv8 inference on incoming simulator frames.
- [ ] Publish detections to a ROS 2 topic from Python.
- [ ] Write C++ ROS 2 subscriber for detection messages.
- [ ] Trigger braking when perception reports a pedestrian/vehicle hazard.
- [ ] Log detection, decision, and braking events for demo replay.

## Phase 4: Berlin-Inspired Portfolio Demo

- [ ] Convert or approximate OpenStreetMap Berlin data for Isaac Sim.
- [ ] Load Berlin-inspired scene into Isaac Sim.
- [ ] Add camera and RTX lidar-style sensor configuration.
- [ ] Record an end-to-end demo video.
- [ ] Add architecture diagram.
- [ ] Write final portfolio README section.
- [ ] Add a short section explaining Isaac Sim vs production NVIDIA AV validation stacks.
