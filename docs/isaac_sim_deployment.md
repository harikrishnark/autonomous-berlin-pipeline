# Isaac Sim VM Deployment Plan

This project is finalized around **NVIDIA Isaac Sim / Omniverse** as the simulator layer. Isaac Sim is the practical choice for a portfolio demo because it is deployable on a cloud GPU VM, supports ROS 2 workflows, exposes realistic RTX sensors, and maps well to autonomy prototyping without claiming production-grade AV validation.

## Positioning

Use this project description in the portfolio:

> Cloud-deployed NVIDIA Isaac Sim autonomy pipeline with ROS 2, synthetic camera/lidar streams, YOLO-based perception, and a control loop that demonstrates hazard detection and braking in simulation.

Do not present this as a full NVIDIA DRIVE production validation stack. Isaac Sim is the hands-on robotics and sensor simulation layer. NVIDIA DRIVE Sim, NuRec, AlpaSim, Alpamayo, and related tooling are the broader AV validation ecosystem to mention as future/industry context.

## VM Target

- Ubuntu 22.04 GPU VM
- RTX-capable NVIDIA GPU preferred: L40S, L4, RTX 4090, RTX 5000/6000 Ada, or similar
- Avoid A100/H100 for this demo because Isaac Sim rendering workflows need RTX graphics support
- Docker
- NVIDIA Container Toolkit
- Isaac Sim container: `nvcr.io/nvidia/isaac-sim:6.0.0`

## Network Ports

Restrict these ports to trusted IPs whenever possible:

```text
TCP 49100  WebRTC signaling
UDP 47998  WebRTC media stream
TCP 8210   Browser viewer when using Docker Compose
```

## Setup Commands

Install Docker:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

Install NVIDIA Container Toolkit:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Validate GPU access:

```bash
docker run --rm --runtime=nvidia --gpus all nvcr.io/nvidia/cuda:12.8.0-base-ubuntu24.04 nvidia-smi
```

Pull Isaac Sim:

```bash
docker pull nvcr.io/nvidia/isaac-sim:6.0.0
```

Create persistent mounts:

```bash
mkdir -p ~/docker/isaac-sim/cache/main
mkdir -p ~/docker/isaac-sim/cache/computecache
mkdir -p ~/docker/isaac-sim/config
mkdir -p ~/docker/isaac-sim/data
mkdir -p ~/docker/isaac-sim/logs
mkdir -p ~/docker/isaac-sim/pkg
mkdir -p ~/.cache/ov/hub
sudo chown -R 1234:1234 ~/docker/isaac-sim ~/.cache/ov/hub
```

Start the container:

```bash
docker run --name isaac-sim --entrypoint bash -it --gpus all \
  -e "ACCEPT_EULA=Y" \
  -e "PRIVACY_CONSENT=Y" \
  --rm --network=host \
  -v ~/docker/isaac-sim/cache/main:/isaac-sim/.cache:rw \
  -v ~/docker/isaac-sim/cache/computecache:/isaac-sim/.nv/ComputeCache:rw \
  -v ~/docker/isaac-sim/logs:/isaac-sim/.nvidia-omniverse/logs:rw \
  -v ~/docker/isaac-sim/config:/isaac-sim/.nvidia-omniverse/config:rw \
  -v ~/docker/isaac-sim/data:/isaac-sim/.local/share/ov/data:rw \
  -v ~/docker/isaac-sim/pkg:/isaac-sim/.local/share/ov/pkg:rw \
  -v ~/.cache/ov/hub:/var/cache/hub:rw \
  -u 1234:1234 \
  nvcr.io/nvidia/isaac-sim:6.0.0
```

Inside the container:

```bash
./isaac-sim.compatibility_check.sh --/app/quitAfter=10 --no-window
PUBLIC_IP=$(curl -s ifconfig.me)
./runheadless.sh \
  --/app/livestream/publicEndpointAddress=$PUBLIC_IP \
  --/app/livestream/port=49100
```

Wait for:

```text
Isaac Sim Full Streaming App is loaded.
```

## Demo Scope

The final demo should show:

- Isaac Sim running on a cloud GPU VM
- WebRTC simulator stream
- Camera and/or RTX lidar sensor output
- Python YOLO perception node
- ROS 2 topic bridge for detections
- C++ control node that triggers braking on hazard detection
- Short recorded demo and architecture diagram

## Mercedes-Facing Narrative

This project should be framed as an autonomy simulation and digital-twin prototype aligned with the NVIDIA Omniverse ecosystem. The strongest story is not "I built production self-driving validation," but:

> I deployed a cloud-hosted Isaac Sim autonomy pipeline and integrated perception, sensor simulation, middleware, and control into a reproducible demo. The project shows awareness of automotive simulation workflows while staying honest about the gap between a portfolio prototype and production AV validation.
