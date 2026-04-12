# Implementation Plan: Autonomous Berlin Pipeline

A phased roadmap for building the full distributed CARLA-based autonomous driving pipeline on a shared cloud VM.

---

## Overview

The pipeline simulates a real-world autonomous vehicle software stack inside the **CARLA** simulator, running entirely on a **RunPod cloud GPU instance**. The AI perception layer (Python/YOLOv8) and the vehicle control layer (C++/ROS 2) communicate over ROS 2 topics within the VM.

**Budget:** $25 USD (RunPod credits) for the initial run.
**Team:** 2 members — all work performed on the shared remote VM via SSH.

---

## Phase 1 — Environment & Foundational Scripts ✅

**Goal:** Establish the base development environment and validate the perception stack.

| Task | Status |
|------|--------|
| Set up Python environment with PyTorch and YOLOv8 on VM | ✅ Done |
| Write base neural network validation script (`brain_perception.py`) | ✅ Done |
| Initialize GitHub repository and push initial code | ✅ Done |
| Write networking socket listener (`network_brain.py`) to receive CARLA camera frames | ✅ Done |
| Write CARLA spawner script (`carla_spawner.py`) | ✅ Done |
| Write mock CARLA client (`mock_carla_client.py`) for offline testing | ✅ Done |

---

## Phase 2 — CARLA Integration

**Goal:** Get CARLA running headless on the VM and streaming camera data.

| Task | Owner | Status |
|------|-------|--------|
| Provision RunPod VM using the "CARLA / Ubuntu VNC Desktop" template | Both | ⬜ |
| Install and launch CARLA Simulator (headless or via VNC) | Both | ⬜ |
| Run `carla_spawner.py` to spawn vehicle, camera, and begin network stream | Both | ⬜ |
| Review and download the generated `simulation_run.mp4` from the VM | Both | ⬜ |

### Notes
- CARLA will be run in **headless mode** on the VM (no display required).
- All streaming and output will be captured to file or piped to the socket listener.
- VNC is available as a fallback for visual debugging.

---

## Phase 3 — Perception-Control Fusion

**Goal:** Connect the AI perception output to the vehicle's control layer inside the VM.

| Task | Owner | Status |
|------|-------|--------|
| Connect `network_brain.py` to the live CARLA camera stream | Both | ⬜ |
| Run YOLOv8 inference on incoming CARLA frames in real time | Both | ⬜ |
| Publish detection results to a ROS 2 topic from the Python node | Both | ⬜ |
| Write a C++ ROS 2 subscriber node to consume detection data | Both | ⬜ |
| Implement emergency braking logic: C++ triggers brake on pedestrian detection | Both | ⬜ |

### Notes
- All components (CARLA, Python perception node, C++ control node) run on the **same VM**.
- ROS 2 Humble is the middleware. No cross-machine networking is required.
- PID-based longitudinal control is the target for Phase 3.

---

## Phase 4 — Berlin Map & Demo

**Goal:** Run the full pipeline on the Berlin OpenStreetMap and produce a portfolio-quality demo.

| Task | Owner | Status |
|------|-------|--------|
| Convert OpenStreetMap Berlin data to CARLA-compatible format | Both | ⬜ |
| Load Berlin map into the CARLA environment on the VM | Both | ⬜ |
| Run an end-to-end simulation: AI detects hazard → C++ triggers braking | Both | ⬜ |
| Record a demo video showing detection + braking event in Berlin map | Both | ⬜ |
| Clean up and document final repository for portfolio | Both | ⬜ |

---

## Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Simulation | CARLA Simulator (cloud VM) |
| Perception | Python 3, PyTorch, YOLOv8, OpenCV |
| Middleware | ROS 2 Humble |
| Control | C++ (C++14/17), PID Controller |
| Infrastructure | RunPod GPU instance (Ubuntu 22.04) |
| Version Control | GitHub |

---

## Budget Guidance

| Item | Estimated Cost |
|------|---------------|
| RunPod GPU pod (development + testing) | ~$0.20–$1.79/hr |
| Full Phase 1–4 run time estimate | ~20–40 hrs |
| **Total estimate** | **~$8–$20 of $25 budget** |

> Shut down (not just pause) the pod when not actively working to avoid idle billing.
