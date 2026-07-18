#!/bin/bash
# System packages for Isaac Sim headless rendering and WebRTC
# RunPod container images reset these on every restart, so run this after any pod reboot!

echo "Installing required system packages (xvfb, ffmpeg, libglu1-mesa, libegl1)..."
apt-get update && apt-get install -y xvfb ffmpeg libglu1-mesa libegl1

echo "Setup complete! Ready for headless rendering."
