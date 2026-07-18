#!/bin/bash
cd /workspace/autonomous-berlin-pipeline
export OMNI_KIT_ACCEPT_EULA=yes
xvfb-run -a -s "-screen 0 1280x720x24" /workspace/isaac_env/bin/python3 -u src/cinematic_city_drive.py
ffmpeg -framerate 20 -pattern_type glob -i "frames_cinematic/*.jpg" -c:v libx264 -pix_fmt yuv420p -y cinematic_output.mp4
