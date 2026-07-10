# Remote Teammate Onboarding (Hari)

Welcome to the shared autonomous driving pipeline project! This guide will get you connected to our cloud GPU VM and help you launch NVIDIA Isaac Sim so you can start contributing.

## 1. Add Your SSH Key to RunPod

You'll need to generate an SSH key and add it to our shared RunPod account to access the VM.

### Generate Key (Mac/Linux)
Open your Terminal and run:
```bash
ssh-keygen -t ed25519 -C "hari-autonomous-berlin" -f ~/.ssh/id_ed25519
```
*(Press Enter twice to skip the passphrase).*

### Copy Public Key
```bash
cat ~/.ssh/id_ed25519.pub
```
*(Copy the entire output starting with `ssh-ed25519 AAAA...`)*

### Add to RunPod
1. Go to [RunPod SSH Settings](https://console.runpod.io/user/settings) and log in.
2. Scroll down to **"SSH public keys"**.
3. Paste your public key **on a new line** (do not delete existing keys).
4. Click **"Update public key"**.

---

## 2. Connect to the Shared VM

We are using a single, shared Ubuntu 22.04 VM with an NVIDIA GPU. 

### SSH Connection Details
```text
Provider: RunPod
VM public IP: 157.157.221.29
Port: 25388
Project path: /workspace/autonomous-berlin-pipeline
```

### Connect via Terminal
Run this command to SSH into the VM:
```bash
ssh -i ~/.ssh/id_ed25519 -p 25388 root@157.157.221.29
```

*(Fallback Proxy: `ssh -i ~/.ssh/id_ed25519 ntu0wjwdd0eb2p-644117ed@ssh.runpod.io`)*

### Verify Connection
Once logged in, verify the GPU is accessible:
```bash
nvidia-smi
```

---

## 3. Starting NVIDIA Isaac Sim

Isaac Sim is our simulation environment. It runs in a Docker container on the VM and streams its interface to your local web browser.

### Step 3a: Launch the Container
SSH into the VM and run the following command to start the container interactively:
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

### Step 3b: Start the Stream
Inside the container terminal, run:
```bash
PUBLIC_IP=$(curl -s ifconfig.me)
./runheadless.sh \
  --/app/livestream/publicEndpointAddress=$PUBLIC_IP \
  --/app/livestream/port=49100
```
Wait until you see: `Isaac Sim Full Streaming App is loaded.`

### Step 3c: Connect from your Browser
1. Open your web browser locally.
2. Download or open the [NVIDIA Omniverse WebRTC Viewer](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/manual_livestream_webrtc.html).
3. Connect using:
   - **Server:** `157.157.221.29`
   - **Port:** `49100`

---

## 4. Working with the Project Code

The repository is already cloned on the VM. 

```bash
cd ~/autonomous-berlin-pipeline
git pull
source venv/bin/activate
```

From here, you can run the perception scripts or work on the ROS 2 integration. 

## Team Rules
- Shut down the VM when nobody is actively working to save credits.
- Announce before stopping containers or rebooting the VM.
- Keep large datasets and videos out of Git.
