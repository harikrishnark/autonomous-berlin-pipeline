# Autonomous Berlin Pipeline

A hybrid autonomous driving software project designed to emulate the production and R&D toolchains used by major automotive manufacturers in Germany (Volkswagen/CARIAD, BMW, Mercedes-Benz, and Tesla). 

This project is a joint effort structured around a **"Divide and Conquer"** architecture, separating AI perception from lower-level safety algorithms to mimic real-world vehicle software layers.

## 🏗 System Architecture

The project is broken into three core layers:

1. **The Brain (Perception & AI):** 
   - **Stack:** Python, PyTorch, OpenCV, YOLOv8
   - **Function:** Processes raw camera/LiDAR data to detect lanes, pedestrians, vehicles, and calculate distance. Currently being developed natively on macOS.
   - **Current status:** Validated YOLOv8 inference for bounding box extraction.

2. **The Nervous System (Middleware):**
   - **Stack:** ROS 2 (Robot Operating System)
   - **Function:** Broadcasts the perception data (e.g., bounding boxes, object distance) from the Python Node over the network so the control logic can read it instantly with safety guarantees.

3. **The Muscle (Vehicle Control):**
   - **Stack:** Modern C++ (C++14/17)
   - **Function:** Safe, mathematical control logic (like PID controllers) that subscribes to the ROS 2 node. If the Python AI spots a pedestrian too close, the C++ code mathematically triggers an emergency braking response.

## 🚀 Getting Started

### Teammate A (AI/Perception) Environment
1. Clone this repository.
2. Create a virtual environment: `python3 -m venv venv` and activate it.
3. Install the dependencies for the vision stack:
```bash
pip install ultralytics opencv-python torch
```
4. Run the perception test: `python src/brain_perception.py`

### Teammate B (Control/ROS 2) Environment
1. Use an Ubuntu 22.04 machine (or WSL2 on Windows).
2. Install [ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html).
3. Clone this repository into your ROS 2 Workspace `src/` folder.
4. Begin writing the C++ subscriber node to listen for data coming from the Python perception pipeline.

## 📁 Repository Structure
* `src/` - Contains the Python (PyTorch) and C++ (ROS 2) nodes.
* `data/` - (Ignored in Git) Stores raw inference images, video datasets, and output visualizations.
