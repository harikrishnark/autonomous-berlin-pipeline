# NVIDIA Isaac Sim VM Deployment on RunPod

This guide details the steps to provision and configure a GPU virtual machine on [RunPod](https://runpod.io) suitable for running the NVIDIA Isaac Sim container.

---

## 1. Selecting a Pod

1.  **Navigate to Secure Cloud:** Log in to your RunPod account and go to the "Secure Cloud" section to deploy a custom machine.
2.  **Choose a GPU:** Select an NVIDIA RTX-series GPU. An **RTX 3080** or higher is recommended for good performance with Isaac Sim. Make sure the GPU has at least 10-12 GB of VRAM.
3.  **Select Template:** In the "Template" search box, find and select the **"RunPod Pytorch 2.3.0"** template. This provides a solid base with PyTorch, CUDA, and the NVIDIA drivers already installed.
4.  **Customize Deployment:**
    - **Container Disk:** Increase to at least `30 GB`.
    - **Volume Disk:** Increase to at least `50 GB`. Isaac Sim and its assets are large.
    - **Set Overrides:** We don't need to override the start command for this template.

5.  **Deploy:** Click "Deploy" and wait for the pod to initialize.

---

## 2. Connecting to the VM

1.  **My Pods:** Once your pod is running, go to the "My Pods" section.
2.  **Connect Button:** Click the "Connect" button on your new pod.
3.  **SSH Connection:** A modal will appear with connection options. The easiest method is to use the "Connect via SSH" command. Copy the full `ssh` command provided.
4.  **Terminal:** Open a terminal on your local machine, paste the command, and press Enter. You will be connected to the VM's shell.

---

## 3. Initial VM Setup

Once connected via SSH, your first steps inside the VM will be to clone the project repository and prepare the environment.

```bash
# Navigate to the persistent volume directory
cd /workspace

# Clone the project repository
git clone https://github.com/harikrishnark/autonomous-berlin-pipeline.git
cd autonomous-berlin-pipeline

# Set up the Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install initial Python dependencies
pip install -r requirements.txt 
```

With these steps completed, the VM is provisioned and ready for the next tasks: installing Docker and the NVIDIA Container Toolkit.

---

## 4. Handling Pod Restarts

Because the RunPod container image resets when a pod stops or restarts, any non-persistent system packages installed via `apt-get` (like the ones required for headless rendering and video encoding) will be lost!

If you ever restart or wake your pod from sleep, **you must perform the following two steps immediately:**

1. **Check for new SSH details:** The pod's IP address and Port will almost certainly change upon restart. Grab the new connection string from the RunPod console before trying to connect.
2. **Reinstall system packages:** We have provided a `setup.sh` script in the root of the workspace. This script reinstalls critical dependencies like `xvfb`, `ffmpeg`, `libglu1-mesa`, and `libegl1`. Run the following command as your very first action after an SSH reconnect:

```bash
cd /workspace/autonomous-berlin-pipeline
chmod +x setup.sh
./setup.sh
```

Without running this script, the Isaac Sim renderer will silently fail and crash during headless execution!