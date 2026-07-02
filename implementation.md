# Implementation Plan: Autonomous Berlin Pipeline

A phased roadmap for building the full NVIDIA Isaac Sim-based autonomous driving prototype on a shared cloud GPU VM.

---

## Overview

The pipeline simulates an autonomous mobility software stack inside **NVIDIA Isaac Sim / Omniverse**, running entirely on a cloud GPU VM. The AI perception layer uses Python, OpenCV, PyTorch, and YOLOv8. The control layer uses C++ and ROS 2. Both layers communicate through ROS 2 topics within the VM.

**Budget:** $25 USD in initial cloud credits.
**Team:** 2 members, with all simulator work performed on the shared remote VM via SSH/WebRTC.

---

## Phase 1: Environment & Foundational Scripts

**Goal:** Establish the base development environment and validate the perception stack.

| Task | Status |
|------|--------|
| Set up Python environment with PyTorch and YOLOv8 on VM | Done |
| Write base neural network validation script `brain_perception.py` | Done |
| Initialize GitHub repository and push initial code | Done |
| Write networking socket listener `network_brain.py` to receive simulator camera frames | Done |
| Write NVIDIA simulator scaffold `src/nvidia_simulator.py` | Done |
| Write mock simulator client `src/mock_carla_client.py` for offline testing | Done |

---

## Phase 2: NVIDIA Isaac Sim Integration

**Goal:** Get NVIDIA Isaac Sim running on the VM and streaming camera/sensor data.

| Task | Owner | Status |
|------|-------|--------|
| Provision GPU VM with RTX-capable NVIDIA GPU support | Both | Open |
| Install Docker and NVIDIA Container Toolkit | Both | Open |
| Pull `nvcr.io/nvidia/isaac-sim:6.0.0` | Both | Open |
| Launch Isaac Sim headless with WebRTC streaming | Both | Open |
| Validate Isaac Sim compatibility check inside the container | Both | Open |
| Run `src/nvidia_simulator.py` or an Isaac Sim script to spawn ego agent, camera, and sensor stream | Both | Open |
| Record and download the first simulator video from the VM | Both | Open |

### Notes

- Isaac Sim runs in headless mode on the VM and streams through WebRTC.
- The target access pattern is SSH for development and WebRTC for visual debugging.
- Streaming ports should be restricted to trusted IPs because the stream does not provide complete production-grade auth/encryption by itself.

---

## Phase 3: Perception-Control Fusion

**Goal:** Connect the AI perception output to the simulated agent control layer.

| Task | Owner | Status |
|------|-------|--------|
| Connect `network_brain.py` to the live Isaac Sim camera stream | Both | Open |
| Run YOLOv8 inference on incoming simulator frames in real time | Both | Open |
| Publish detection results to a ROS 2 topic from the Python node | Both | Open |
| Write a C++ ROS 2 subscriber node to consume detection data | Both | Open |
| Implement emergency braking logic on pedestrian/vehicle hazard detection | Both | Open |

### Notes

- All components run on the same VM for the first demo.
- ROS 2 Humble is the middleware target.
- The first control goal is longitudinal braking, not full autonomous driving.

---

## Phase 4: Berlin-Inspired Demo

**Goal:** Produce a portfolio-quality demo that feels relevant to German automotive work.

| Task | Owner | Status |
|------|-------|--------|
| Convert or approximate Berlin OpenStreetMap data for an Isaac Sim scene | Both | Open |
| Load the Berlin-inspired scene into Isaac Sim on the VM | Both | Open |
| Run an end-to-end simulation: AI detects hazard, C++ triggers braking | Both | Open |
| Record a demo video showing sensor stream, detection, and braking event | Both | Open |
| Add architecture diagram and final portfolio documentation | Both | Open |

---

## Tech Stack Summary

| Layer | Technology |
|-------|------------|
| Simulation | NVIDIA Isaac Sim / Omniverse on cloud GPU VM |
| Perception | Python 3, PyTorch, YOLOv8, OpenCV |
| Middleware | ROS 2 Humble |
| Control | C++14/17, ROS 2 subscriber, braking logic |
| Infrastructure | Ubuntu 22.04 GPU VM, Docker, NVIDIA Container Toolkit |
| Version Control | GitHub |

---

## Mercedes-Facing Portfolio Narrative

This project should be framed as an autonomy simulation and digital-twin prototype aligned with the NVIDIA Omniverse ecosystem:

> I deployed a cloud-hosted Isaac Sim autonomy pipeline and integrated perception, sensor simulation, middleware, and control into a reproducible demo. The project shows awareness of automotive simulation workflows while staying honest about the gap between a portfolio prototype and production AV validation.

---

## Budget Guidance

| Item | Estimated Cost |
|------|----------------|
| GPU VM development and testing | About $0.20-$1.79/hr depending on GPU |
| Full first demo run time estimate | 10-25 hrs |
| Estimated total | About $8-$25 |

Shut down the VM when not actively working to avoid idle billing.
