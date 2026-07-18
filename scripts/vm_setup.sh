#!/usr/bin/env bash
# =============================================================================
# vm_setup.sh — Automated RunPod VM Setup for Autonomous Berlin Pipeline
# =============================================================================
# Run this script after SSH'ing into your RunPod GPU pod.
# Usage: bash vm_setup.sh
# =============================================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log()   { echo -e "${GREEN}[✔]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✘]${NC} $1"; }
info()  { echo -e "${BLUE}[→]${NC} $1"; }
header(){ echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "${BLUE}  $1${NC}"; echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"; }

# ─────────────────────────────────────────────────────────────────────────────
header "Step 1/7: System Check"
# ─────────────────────────────────────────────────────────────────────────────

info "Hostname: $(hostname)"
info "OS: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '"' || echo 'Unknown')"

if command -v nvidia-smi &>/dev/null; then
    log "NVIDIA driver found"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
else
    error "nvidia-smi not found! This pod may not have GPU support."
    exit 1
fi

# ─────────────────────────────────────────────────────────────────────────────
header "Step 2/7: Clone Project Repository"
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_DIR="/workspace/autonomous-berlin-pipeline"

if [ -d "$PROJECT_DIR" ]; then
    warn "Project directory already exists. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull || warn "Git pull failed — continuing with existing code"
else
    info "Cloning repository..."
    cd /workspace
    git clone https://github.com/harikrishnark/autonomous-berlin-pipeline.git
    cd "$PROJECT_DIR"
    log "Repository cloned successfully"
fi

# ─────────────────────────────────────────────────────────────────────────────
header "Step 3/7: Python Environment"
# ─────────────────────────────────────────────────────────────────────────────

if [ ! -d "$PROJECT_DIR/venv" ]; then
    info "Creating Python virtual environment..."
    python3 -m venv venv
    log "Virtual environment created"
else
    warn "Virtual environment already exists"
fi

source venv/bin/activate
info "Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet ultralytics opencv-python torch
log "Python dependencies installed"

# Quick validation
python3 -c "import torch; print(f'PyTorch {torch.__version__}, CUDA available: {torch.cuda.is_available()}')"

# ─────────────────────────────────────────────────────────────────────────────
header "Step 4/7: Docker Setup"
# ─────────────────────────────────────────────────────────────────────────────

if command -v docker &>/dev/null; then
    log "Docker already installed: $(docker --version)"
else
    info "Installing Docker..."
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sh /tmp/get-docker.sh
    rm /tmp/get-docker.sh
    log "Docker installed"
fi

# Ensure docker daemon is running
if ! docker info &>/dev/null 2>&1; then
    info "Starting Docker daemon..."
    service docker start 2>/dev/null || dockerd &>/dev/null &
    sleep 3
fi

# ─────────────────────────────────────────────────────────────────────────────
header "Step 5/7: NVIDIA Container Toolkit"
# ─────────────────────────────────────────────────────────────────────────────

if dpkg -l nvidia-container-toolkit &>/dev/null 2>&1; then
    log "NVIDIA Container Toolkit already installed"
else
    info "Installing NVIDIA Container Toolkit..."

    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
        gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg 2>/dev/null

    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        tee /etc/apt/sources.list.d/nvidia-container-toolkit.list > /dev/null

    apt-get update -qq
    apt-get install -y -qq nvidia-container-toolkit
    nvidia-ctk runtime configure --runtime=docker
    
    # Restart docker to pick up nvidia runtime
    service docker restart 2>/dev/null || true
    sleep 2

    log "NVIDIA Container Toolkit installed and configured"
fi

# Validate GPU passthrough in Docker
info "Validating GPU passthrough in Docker..."
if docker run --rm --gpus all nvcr.io/nvidia/cuda:12.8.0-base-ubuntu24.04 nvidia-smi &>/dev/null; then
    log "GPU passthrough working!"
    docker run --rm --gpus all nvcr.io/nvidia/cuda:12.8.0-base-ubuntu24.04 nvidia-smi
else
    error "GPU passthrough failed. Check NVIDIA Container Toolkit installation."
    warn "Attempting to continue anyway..."
fi

# ─────────────────────────────────────────────────────────────────────────────
header "Step 6/7: Pull Isaac Sim Container"
# ─────────────────────────────────────────────────────────────────────────────

ISAAC_IMAGE="nvcr.io/nvidia/isaac-sim:6.0.0"

info "Pulling Isaac Sim container image (this may take 10-20 minutes)..."
info "Image: $ISAAC_IMAGE"

docker pull "$ISAAC_IMAGE" && log "Isaac Sim image pulled successfully" || {
    error "Failed to pull Isaac Sim image."
    warn "You may need to log in to NGC first:"
    warn "  docker login nvcr.io"
    warn "  Username: \$oauthtoken"
    warn "  Password: <your NGC API key>"
    warn "Get your NGC API key at: https://ngc.nvidia.com/setup"
}

# ─────────────────────────────────────────────────────────────────────────────
header "Step 7/7: Create Persistent Mount Directories"
# ─────────────────────────────────────────────────────────────────────────────

info "Creating Isaac Sim mount directories..."
mkdir -p ~/docker/isaac-sim/cache/main
mkdir -p ~/docker/isaac-sim/cache/computecache
mkdir -p ~/docker/isaac-sim/config
mkdir -p ~/docker/isaac-sim/data
mkdir -p ~/docker/isaac-sim/logs
mkdir -p ~/docker/isaac-sim/pkg
mkdir -p ~/.cache/ov/hub
chown -R 1234:1234 ~/docker/isaac-sim ~/.cache/ov/hub 2>/dev/null || true
log "Mount directories created"

# ─────────────────────────────────────────────────────────────────────────────
header "Setup Complete!"
# ─────────────────────────────────────────────────────────────────────────────

PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "<UNKNOWN>")

echo ""
log "VM is ready for Isaac Sim!"
echo ""
info "Public IP: $PUBLIC_IP"
echo ""
echo -e "${GREEN}To start Isaac Sim, run:${NC}"
echo ""
cat <<'LAUNCH'
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
LAUNCH

echo ""
echo -e "${GREEN}Then inside the container:${NC}"
echo ""
cat <<INSIDE
./isaac-sim.compatibility_check.sh --/app/quitAfter=10 --no-window
./runheadless.sh \\
  --/app/livestream/publicEndpointAddress=$PUBLIC_IP \\
  --/app/livestream/port=49100
INSIDE

echo ""
info "Connect via browser: http://$PUBLIC_IP:49100"
echo ""
warn "Remember: STOP the pod when you're done to save credits!"
echo ""
