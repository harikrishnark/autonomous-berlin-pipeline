# Remote Teammate Onboarding

Use this file to onboard a teammate onto the shared GPU VM. Fill in the placeholders out-of-band through a private channel. Do not commit private keys, tokens, passwords, or provider secrets.

## Connection Details

```text
Provider: RunPod
VM name: PyTorch Pod
VM public IP: 157.157.221.29
SSH proxy endpoint: ntu0wjwdd0eb2p-644117ed@ssh.runpod.io
SSH direct TCP: root@157.157.221.29 -p 25388
SSH key path: ~/.ssh/id_ed25519
Project path on VM: /workspace/autonomous-berlin-pipeline
Repository URL: https://github.com/harikrishnark/autonomous-berlin-pipeline.git
Provider notes: Web terminal is exposed on port 19123 through the proxied RunPod URL.
```

## SSH Command

Primary Direct TCP (Recommended for VS Code/Antigravity):

```bash
chmod 600 ~/.ssh/id_ed25519
ssh -i ~/.ssh/id_ed25519 -p 25388 root@157.157.221.29
```

Proxy fallback:

```bash
ssh -i ~/.ssh/id_ed25519 ntu0wjwdd0eb2p-644117ed@ssh.runpod.io
```

## First Login Checklist

```bash
hostname
nvidia-smi
docker --version
docker ps
```

Confirm that the GPU is visible before starting Isaac Sim or any training/inference process.

## Project Setup

```bash
cd ~
git clone <REPO_URL> autonomous-berlin-pipeline
cd autonomous-berlin-pipeline

python3 -m venv venv
source venv/bin/activate
pip install ultralytics opencv-python torch

python src/brain_perception.py
```

If the repo is private, configure GitHub SSH access, HTTPS credentials, or a deploy key before cloning.

If the repo already exists on the VM:

```bash
cd ~/autonomous-berlin-pipeline
git pull
source venv/bin/activate
```

## Isaac Sim Access Notes

Isaac Sim is expected to run inside the NVIDIA container:

```bash
docker pull nvcr.io/nvidia/isaac-sim:6.0.0
```

Required streaming ports:

```text
TCP 49100  WebRTC signaling
UDP 47998  WebRTC media stream
TCP 8210   Browser viewer, if using Docker Compose
```

Restrict these ports to trusted IPs whenever the provider supports firewall rules.

After Isaac Sim is running headless, connect with the Isaac Sim WebRTC Streaming Client or browser viewer:

```text
Server/IP: <VM_PUBLIC_IP>
Port: 49100
```

Wait until the Isaac Sim logs say the streaming app is loaded before connecting.

## Team Rules

- Do not commit private SSH keys, API tokens, RunPod credentials, or NVIDIA NGC credentials.
- Shut down the VM when nobody is actively working.
- Announce before stopping containers or rebooting the VM.
- Pull before editing and push after a working milestone.
- Keep large datasets, videos, and simulator cache files out of Git unless explicitly needed.
- Rotate credentials immediately if a key or token is accidentally shared.

## Useful Project Docs

- `README.md`: project overview and portfolio positioning
- `implementation.md`: phased roadmap
- `TODO.md`: active checklist
- `docs/isaac_sim_deployment.md`: Isaac Sim VM/container deployment plan
