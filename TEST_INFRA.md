# E2E Test Infrastructure: Autonomous Berlin Pipeline

This document details the requirement-driven, opaque-box end-to-end (E2E) testing framework designed for the Autonomous Berlin Pipeline. The test suite operates locally on the developer machine and targets the remote NVIDIA Isaac Sim GPU VM via secure shell (SSH) interfaces.

---

## 1. Test Strategy & Objectives

The testing approach follows an **opaque-box E2E paradigm**. Instead of instrumenting internal simulator loops or perception class models, the framework validates system behavior from the outside by:
1. Verifying critical service availability (ports, configuration files, and model presence).
2. Spawning and executing simulator processes via headless wrappers (`xvfb-run`).
3. Intercepting and tunneling the network loopback socket endpoints.
4. Stress-testing boundary conditions, invalid configurations, and performance limits.

---

## 2. Test Architecture

The E2E test runner is located in the local `.venv` environment and connects to the remote host over SSH.

```
       Local Workstation                            Remote RunPod VM
+-----------------------------+             +-------------------------------+
| Pytest E2E Test Suite       |             | Isaac Sim Headless Instance   |
| (test_webrtc_stream.py)     |             | (cinematic_city_drive.py)     |
|                             |             +---------------+---------------+
|  +-----------------------+  |             |               |               |
|  | Paramiko SSH Client   |=== SSH (24034) ===> Bash commands  |               |
|  +-----------------------+  |             |               |               |
|  | Direct-TCP Tunneling  |=== Loopback ======> WebRTC Signaling (49100)    |
|  +-----------------------+  |             | AI perception Server (5005)   |
+-----------------------------+             +-------------------------------+
```

### Key Ports Tested
- **TCP 49100**: Isaac Sim WebRTC signaling server port.
- **UDP 47998**: WebRTC media transmission.
- **TCP 5005**: AI perception server (YOLOv8 socket).

---

## 3. Test Cases Classification (39 Distinct Test Cases)

### Tier 1: Feature Coverage (15 Test Cases)
Verifies the essential happy paths of the system, including SSH connectivity, GPU access, file locations, and port availability.
- **`test_t1_ssh_connection`**: Direct SSH connection and handshake.
- **`test_t1_remote_gpu_presence`**: Verifies GPU availability (`nvidia-smi -L`).
- **`test_t1_remote_nvidia_driver`**: Confirms valid NVIDIA driver configuration.
- **`test_t1_remote_python_path`**: Verifies isolated python virtual environment presence.
- **`test_t1_remote_isaacsim_import`**: Assures the `isaacsim` library loads successfully.
- **`test_t1_remote_project_dir_exists`**: Confirms path to `/workspace/autonomous-berlin-pipeline`.
- **`test_t1_network_brain_script_exists`**: Checks path to `src/network_brain.py`.
- **`test_t1_cinematic_drive_script_exists`**: Checks path to `src/cinematic_city_drive.py`.
- **`test_t1_webrtc_stream_script_exists`**: Checks path to `src/test_stream.py`.
- **`test_t1_yolov8_model_exists`**: Assures weights `yolov8n.pt` are present.
- **`test_t1_sim_run_shell_script`**: Confirms wrapper shell script path `run_sim.sh`.
- **`test_t1_xvfb_installed`**: Verifies `xvfb-run` exists.
- **`test_t1_remote_port_49100_free`**: Confirms WebRTC port 49100 is not blocked.
- **`test_t1_remote_port_5005_free`**: Confirms AI port 5005 is not blocked.
- **`test_t1_mock_carla_client_file_exists`**: Checks path to `src/mock_carla_client.py`.

### Tier 2: Boundary & Corner Cases (17 Test Cases)
Validates error pathways, invalid configurations, socket collisions, and abnormal client inputs.
- **`test_t2_ssh_invalid_host`**: Graceful failure when IP is unreachable.
- **`test_t2_ssh_invalid_port`**: Graceful failure when port is incorrect.
- **`test_t2_ssh_invalid_user`**: Graceful failure when authentication username is bad.
- **`test_t2_ssh_invalid_key`**: Rejection of unauthorized keys.
- **`test_t2_remote_command_syntax_error`**: Ensures non-zero exit codes are bubbled up for bash errors.
- **`test_t2_remote_python_invalid_syntax`**: Confirms python failures log traceback and return 1.
- **`test_t2_remote_missing_file_error`**: Checks handling of missing files.
- **`test_t2_network_brain_invalid_host_bind`**: Assures bind fails on invalid IPs.
- **`test_t2_network_brain_invalid_port_bind`**: Assures bind fails on out-of-range ports.
- **`test_t2_network_brain_port_collision`**: Tests `OSError` handling on duplicate port binding.
- **`test_t2_remote_kill_nonexistent_process`**: Verifies kill errors when PID is invalid.
- **`test_t2_isaac_sim_no_display_error`**: Assures simulator rejects starting without visual wrapper.
- **`test_t2_client_frame_header_too_small`**: Handles short header packets (< 4 bytes) without crash.
- **`test_t2_client_frame_header_too_large`**: Rejects abnormally large headers to avoid memory leaks.
- **`test_t2_client_partial_frame_send`**: Confirms server breaks connection cleanly on missing payload bytes.
- **`test_t2_client_disconnect_abruptly`**: Assures socket teardown works under abrupt close events.
- **`test_t2_ssh_tunnel_disconnect_and_reconnect`**: Tests recovery and re-opening of SSH channels.

### Tier 3: Cross-Feature Interactions (3 Test Cases)
Verifies parallel functionality and loopbacks combining different parts of the pipeline.
- **`test_t3_concurrent_signaling_and_perception_ports`**: Parallel channel querying.
- **`test_t3_ssh_tunnel_data_transfer`**: Forwards local port to remote port over SSH and matches payload.
- **`test_t3_simulator_perception_loopback`**: Simulates mock client frame transmission and perception command feedback in a concurrent loop.

### Tier 4: Real-World Workloads (4 Test Cases)
Validates real performance constraints, active simulation runs, and lifecycle milestones.
- **`test_t4_perception_processing_throughput`**: Benchmarks YOLOv8 latency to be under 150ms per frame.
- **`test_t4_webrtc_signaling_http_handshake`**: Assures WebRTC signaling endpoint responds to handshakes.
- **`test_t4_continuous_simulation_drive`**: Spawns short (10 frames) Isaac Sim drive headless and verifies completion.
- **`test_t4_pipeline_full_lifecycle_run`**: Boots perception, executes simulation, verifies BRAKE trigger, and tears down.
- **`test_t4_multiple_perception_clients_sequential`**: Handles multiple client threads connecting one after another.

---

## 4. How to Run the Tests

### Prerequisites
1. Local virtual environment with `pytest` and `paramiko` installed:
   ```bash
   pip install pytest paramiko opencv-python numpy cryptography
   ```
2. Valid SSH Private key matching the remote RunPod VM target.

### Execution
Run the full test suite locally:
```bash
pytest -v tests/e2e/test_webrtc_stream.py
```

To run a specific test:
```bash
pytest -v tests/e2e/test_webrtc_stream.py::test_t1_ssh_connection
```
