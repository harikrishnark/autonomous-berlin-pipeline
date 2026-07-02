# Remote Teammate Onboarding

Use this file to onboard a teammate onto the shared GPU VM. Fill in the placeholders out-of-band through a private channel. Do not commit private keys, tokens, passwords, or provider secrets.

## Connection Details

```text
Provider: <RUNPOD_OR_OTHER_PROVIDER>
VM name: <VM_NAME>
VM public IP: <VM_PUBLIC_IP>
SSH user: <SSH_USER>
SSH port: <SSH_PORT>
SSH key path: <SSH_KEY_PATH>
Project path on VM: ~/autonomous-berlin-pipeline
Repository URL: <REPO_URL>
Provider notes: <RUNPOD_OR_PROVIDER_NOTES>
```

## SSH Command

```bash
chmod 600 <SSH_KEY_PATH>
ssh -i <SSH_KEY_PATH> -p <SSH_PORT> <SSH_USER>@<VM_PUBLIC_IP>
```

If the provider gives a complete SSH command, use that exact command and save it privately.

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
