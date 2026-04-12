# Task List: Distributed CARLA Pipeline

Because of macOS hardware constraints, the project is structured as a Distributed Client/Server model.

- `[x]` **Phase 1: Environment & Foundational Scripts**
  - `[x]` **Teammate A (Mac/AI):** Set up Python environment with PyTorch and YOLOv8.
  - `[x]` **Teammate A (Mac/AI):** Write base neural network validation script (`brain_perception.py`).
  - `[x]` **Both:** Initialize GitHub repository and commit code.
  - `[x]` **Teammate A (Mac/AI):** Write Networking Socket Listener (`network_brain.py`) to receive CARLA camera images over the internet.
  - `[ ]` **Teammate B:** Rent RunPod Virtual Machine and configure it (Docker vs Raw Ubuntu option).

- `[ ]` **Phase 2: CARLA Integration**
  - `[ ]` **Teammate B:** Rent RunPod Virtual Machine using the "CARLA / Ubuntu VNC Desktop" Template.
  - `[ ]` **Teammate B:** Install CARLA Simulator headless or start it via the VNC environment.
  - `[ ]` **Teammate B:** Run the `carla_spawner.py` script we wrote to spawn a car, camera, and start streaming to the network socket.
  - `[ ]` **Teammate B:** Review the generated `simulation_run.mp4` video locally on the VM and download it.

- `[ ]` **Phase 3: The Fusion**
  - `[ ]` **Both:** Open the Cloud VM networking ports so Teammate A's Mac receives the video stream.
  - `[ ]` **Teammate A:** Run `network_brain.py` live against the incoming cloud stream.
  - `[ ]` **Teammate B:** Program the car in CARLA to hit the brakes when Teammate A's AI detects an object.

- `[ ]` **Phase 4: Optimization & Output**
  - `[ ]` Convert OpenStreetMap Berlin data and load it into the cloud CARLA environment.
  - `[ ]` Record a demo video of the AI triggering the braking system in the Berlin simulation map.
