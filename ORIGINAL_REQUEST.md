# Original User Request

## Initial Request — 2026-07-11T01:31:02+02:00

# Teamwork Project Prompt

Update the `cinematic_city_drive.py` script to enable and configure the WebRTC extension. Verify that the headless Isaac Sim execution streams its output live to a browser.

Working directory: `c:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline`
Integrity mode: benchmark

## Requirements

### R1. Enable WebRTC
Update `src/cinematic_city_drive.py` to correctly load and configure the Omniverse WebRTC streaming extension so that it captures the simulation rendering.

### R2. Network Tunneling
Configure and document an SSH tunnel command to securely forward the required WebRTC ports from the remote RunPod VM to the local machine (`localhost`).

## Acceptance Criteria

### Verification
- [ ] **RunPod Endpoint Test:** A script or curl command must verify that the WebRTC signalling server is actively listening on its expected port on the RunPod while the simulation runs.
- [ ] **Tunnel Verification:** An SSH tunnel command is provided, and executing it successfully binds the local ports without error.
- [ ] **No Simulation Crash:** The `cinematic_city_drive.py` script must initialize the environment and vehicle fully without segfaulting or crashing due to the WebRTC extension.
