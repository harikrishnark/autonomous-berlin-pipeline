## Forensic Audit Report

**Work Product**: `src/cinematic_city_drive.py` and `tests/e2e/test_webrtc_stream.py`
**Profile**: General Project
**Verdict**: CLEAN

### Phase Results
- **Hardcoded test results detection**: PASS — Checked the project repository for hardcoded test results or expected values designed to cheat. The perception system retrieves live outputs directly from real YOLOv8 models.
- **Facade detection**: PASS — Verified there is no local mock version of the `ultralytics` package in `src/` or `tests/`. The real `ultralytics` package installed in the python virtual environment is used for all object detection.
- **Pre-populated artifact detection**: PASS — Verified no logs, output files, or verification artifacts exist in the repository that predate the test runs.
- **Behavioral verification (Build & Run)**: PASS — Executed the E2E test runner command `.venv\Scripts\python -m pytest -v tests/e2e/test_webrtc_stream.py` and confirmed that all 40 test cases passed with exit code 0.
- **WebRTC Settings Verification**: PASS — Checked `src/cinematic_city_drive.py` and verified the WebRTC settings are authentic, including the correct port configuration (`49100`) and the extension enabling statement (`omni.services.streamclient.webrtc`).
- **YOLOv8 Dynamic Inference Verification**: PASS — Executed YOLOv8 inference dynamically on `bus.jpg` using `venv\Scripts\python.exe src/brain_perception.py` and confirmed real-world detections (4 persons, 1 bus, 1 stop sign) are dynamically predicted.

### Evidence

#### 1. Test Execution Output (40/40 tests passed)
```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline
collecting ... collected 40 items

tests/e2e/test_webrtc_stream.py::test_t1_ssh_connection PASSED           [  2%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_gpu_presence PASSED      [  5%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_nvidia_driver PASSED     [  7%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_python_path PASSED       [ 10%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_isaacsim_import PASSED   [ 12%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_project_dir_exists PASSED [ 15%]
tests/e2e/test_webrtc_stream.py::test_t1_network_brain_script_exists PASSED [ 17%]
tests/e2e/test_webrtc_stream.py::test_t1_cinematic_drive_script_exists PASSED [ 20%]
tests/e2e/test_webrtc_stream.py::test_t1_webrtc_stream_script_exists PASSED [ 22%]
tests/e2e/test_webrtc_stream.py::test_t1_yolov8_model_exists PASSED      [ 25%]
tests/e2e/test_webrtc_stream.py::test_t1_sim_run_shell_script PASSED     [ 27%]
tests/e2e/test_webrtc_stream.py::test_t1_xvfb_installed PASSED           [ 30%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_port_49100_free PASSED   [ 32%]
tests/e2e/test_webrtc_stream.py::test_t1_remote_port_5005_free PASSED    [ 35%]
tests/e2e/test_webrtc_stream.py::test_t1_mock_carla_client_file_exists PASSED [ 37%]
tests/e2e/test_webrtc_stream.py::test_t2_ssh_invalid_host PASSED         [ 40%]
tests/e2e/test_webrtc_stream.py::test_t2_ssh_invalid_port PASSED         [ 42%]
tests/e2e/test_webrtc_stream.py::test_t2_ssh_invalid_user PASSED         [ 45%]
tests/e2e/test_webrtc_stream.py::test_t2_ssh_invalid_key PASSED          [ 47%]
tests/e2e/test_webrtc_stream.py::test_t2_remote_command_syntax_error PASSED [ 50%]
tests/e2e/test_webrtc_stream.py::test_t2_remote_python_invalid_syntax PASSED [ 52%]
tests/e2e/test_webrtc_stream.py::test_t2_remote_missing_file_error PASSED [ 55%]
tests/e2e/test_webrtc_stream.py::test_t2_network_brain_invalid_host_bind PASSED [ 57%]
tests/e2e/test_webrtc_stream.py::test_t2_network_brain_invalid_port_bind PASSED [ 60%]
tests/e2e/test_webrtc_stream.py::test_t2_network_brain_port_collision PASSED [ 62%]
tests/e2e/test_webrtc_stream.py::test_t2_remote_kill_nonexistent_process PASSED [ 65%]
tests/e2e/test_webrtc_stream.py::test_t2_isaac_sim_no_display_error PASSED [ 67%]
tests/e2e/test_webrtc_stream.py::test_t2_client_frame_header_too_small PASSED [ 70%]
tests/e2e/test_webrtc_stream.py::test_t2_client_frame_header_too_large PASSED [ 72%]
tests/e2e/test_webrtc_stream.py::test_t2_client_partial_frame_send PASSED [ 75%]
tests/e2e/test_webrtc_stream.py::test_t2_client_disconnect_abruptly PASSED [ 77%]
tests/e2e/test_webrtc_stream.py::test_t2_ssh_tunnel_disconnect_and_reconnect PASSED [ 80%]
tests/e2e/test_webrtc_stream.py::test_t3_concurrent_signaling_and_perception_ports PASSED [ 82%]
tests/e2e/test_webrtc_stream.py::test_t3_ssh_tunnel_data_transfer PASSED [ 85%]
tests/e2e/test_webrtc_stream.py::test_t3_simulator_perception_loopback PASSED [ 87%]
tests/e2e/test_webrtc_stream.py::test_t4_perception_processing_throughput PASSED [ 90%]
tests/e2e/test_webrtc_stream.py::test_t4_webrtc_signaling_http_handshake PASSED [ 92%]
tests/e2e/test_webrtc_stream.py::test_t4_continuous_simulation_drive PASSED [ 95%]
tests/e2e/test_webrtc_stream.py::test_t4_pipeline_full_lifecycle_run PASSED [ 97%]
tests/e2e/test_webrtc_stream.py::test_t4_multiple_perception_clients_sequential PASSED [100%]

============================= 40 passed in 20.21s =============================
```

#### 2. YOLOv8 Dynamic Inference Output
Executing `venv\Scripts\python.exe src/brain_perception.py`:
```
Loading PyTorch & YOLOv8 model for Autonomous Perception...
Running Inference on https://ultralytics.com/images/bus.jpg...

Found https://ultralytics.com/images/bus.jpg locally at bus.jpg
image 1/1 C:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline\bus.jpg: 640x480 4 persons, 1 bus, 1 stop sign, 82.3ms
Speed: 3.7ms preprocess, 82.3ms inference, 1.6ms postprocess per image at shape (1, 3, 640, 480)

--- DETECTED OBJECTS TO SEND TO C++ ROS NODE ---
Detected: bus        | Confidence: 0.87 | Bounding Box: [22.9, 231.3, 805.0, 756.8]
Detected: person     | Confidence: 0.87 | Bounding Box: [48.6, 398.6, 245.3, 902.7]
Detected: person     | Confidence: 0.85 | Bounding Box: [669.5, 392.2, 809.7, 877.0]
Detected: person     | Confidence: 0.83 | Bounding Box: [221.5, 405.8, 345.0, 857.5]
Detected: person     | Confidence: 0.26 | Bounding Box: [0.0, 550.5, 63.0, 873.4]
Detected: stop sign  | Confidence: 0.26 | Bounding Box: [0.1, 254.5, 32.6, 324.9]

Saved visualization to: data\perception_output.jpg
```
