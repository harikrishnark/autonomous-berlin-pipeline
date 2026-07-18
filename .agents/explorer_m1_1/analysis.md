# Milestone 1: VM and Codebase Exploration Analysis

This report documents the local system and remote RunPod VM configuration, connection details, codebase layout, and python virtual environments.

## 1. Remote VM Connectivity and SSH Configuration

### Local SSH Configuration
The local SSH configuration is defined in the SSH configuration file at `C:\Users\aksha\.ssh\config`:
```ssh
Host runpod
    HostName 157.157.221.29
    Port 24034
    User root
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
```

### Connection Details
- **Hostname (IP)**: `157.157.221.29`
- **Active SSH Port**: `24034`
- **Username**: `root`
- **Identity File**: `C:\Users\aksha\.ssh\id_ed25519` (Local ED25519 SSH private key)
- **Strict Host Key Checking**: Disabled (`no`)

### Connectivity Verification
We verified SSH connectivity using the following command from the local powershell terminal:
```powershell
ssh -o ConnectTimeout=5 runpod "echo 'connection successful'"
```
**Result**:
```
connection successful
```
This confirms that the private key matches the authorized keys on the remote RunPod VM, and connection can be made successfully.

---

## 2. Remote Docker and Isaac Sim Container Status

- **Docker Status**: Docker is **not** installed on the remote system.
  - Running `docker ps -a` returns: `bash: line 1: docker: command not found`.
  - The presence of the `.dockerenv` file at the root directory (`/`) indicates that the remote VM itself runs inside a Docker container managed by RunPod.
- **Isaac Sim Status**: Isaac Sim is installed natively as a Python package (`isaacsim==5.1.0.0`) inside the `/workspace/isaac_env` Python virtual environment.
- **Active Processes**:
  An active AI perception server is running in a tmux session named `brain`:
  - Command: `/workspace/isaac_env/bin/python3 -u src/network_brain.py 2>&1 | tee /workspace/brain.log`
  - Log output (`/workspace/brain.log`) confirms the simulator connects and drives or brakes based on object detection:
    ```
    ✅ Simulator connected from: ('127.0.0.1', 48216)
    🟢 Path clear. Sending DRIVE command.
    ...
    🚨 Obstacle close (Y: 412.3)! Sending BRAKE command to simulator.
    ```

---

## 3. Codebase Layout and Git Synchronization

Both the local and remote repositories are synchronized to the exact same git commit:
- **Commit Hash**: `0f43f0ad7b5aedef17f2a403c36815eceb0f2678`
- **Commit Author**: Akshay <akshayanil4@gmail.com>
- **Commit Message**: `Fix camera init order to fix headless Replicator bugs`

### Local Codebase
- **Directory**: `c:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline`
- **Local-Only Files / Untracked Files**:
  - `src/generate_test_video.py` (Local utility to mock video generation)
  - `.venv/` and `venv/` (Local Python environments)
  - `.agents/` metadata (Plans, handoffs, and agent briefing/requests)
  - Untracked artifacts: `cinematic_output.mp4`, `simulation_output.mp4`, `simulation_output_fixed.mp4`, `simulation_output_base64.txt`, `web-debrief/`
- **Git Status**:
  ```
  On branch main
  Your branch is up to date with 'origin/main'.
  You are currently rebasing.
    (all conflicts fixed: run "git rebase --continue")
  Changes not staged for commit:
    TODO.md
    docs/remote_teammate_onboarding.md
    src/create_city_scene.py
  ```

### Remote Codebase
- **Directory**: `/workspace/autonomous-berlin-pipeline`
- **Remote-Only Files / Untracked Files**:
  - `/workspace/check_assets.py`, `check_cars.py`, `check_outdoor.py`, `check_rivermark.py` (Asset validation helper scripts outside the repo)
  - `src/check_environments.py` (Asset XML S3 metadata scraper)
  - `/workspace/brain.log` and `/workspace/isaac_stream.log` (Runtime log files)
  - Untracked folders: `frames/` and `frames_cinematic/` (containing JPG image frames generated during simulation)
  - Untracked artifacts: `cinematic_output.mp4`, `sim_cinematic.log`, `simulation_output.avi`, `simulation_output.mp4`, `simulation_output_fixed.mp4`, `xvfb_out.log`, `yolov8n.pt`, `urban_construction_scene.usd`

---

## 4. Python Virtual Environments

### Remote Environment (`/workspace/isaac_env`)
- **Type**: Python 3.11 Virtual Environment (`venv`)
- **Python Version**: `3.11.10`
- **Base Python Interpreter**: `/usr/bin/python3.11`
- **Key Installed Packages**:
  - `isaacsim` (Version `5.1.0.0`)
  - `torch` (Version `2.7.0`)
  - `torchvision` (Version `0.22.0`)
  - `ultralytics` (Version `8.4.92` for YOLOv8 perception)
  - `opencv-python` (Version `4.10.0.84`)
  - `numpy` (Version `1.26.0`)
  - `fastapi` (Version `0.115.7`)

### Local Environments
There are two local python virtual environments inside the repository root folder:

1. **Local `.venv` (`c:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline\.venv`)**
   - **Type**: Python 3.12 Virtual Environment
   - **Python Version**: `3.12.10`
   - **Base Python Interpreter**: `C:\Users\aksha\AppData\Local\Programs\Python\Python312\python.exe`
   - **Key Installed Packages**:
     - `numpy` (Version `2.5.0`)
     - `opencv-python` (Version `5.0.0.93`)
     - (No PyTorch, YOLOv8, or Isaac Sim)

2. **Local `venv` (`c:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline\venv`)**
   - **Type**: Python 3.12 Virtual Environment
   - **Python Version**: `3.12.10`
   - **Base Python Interpreter**: `C:\Users\aksha\AppData\Local\Programs\Python\Python312\python.exe`
   - **Key Installed Packages**:
     - `torch` (Version `2.12.1` - note: placeholder/stub version)
     - `torchvision` (Version `0.27.1`)
     - `ultralytics` (Version `8.4.84`)
     - `opencv-python` (Version `5.0.0.93`)
     - `numpy` (Version `2.5.0`)
     - `polars` (Version `1.42.1`)
     - (No `isaacsim` package installed locally)
