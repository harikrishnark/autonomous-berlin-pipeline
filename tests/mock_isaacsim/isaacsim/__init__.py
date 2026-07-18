import os
import sys

class SimulationApp:
    def __init__(self, config=None, *args, **kwargs):
        # Simulate Isaac Sim checking for display/X11
        if not os.environ.get("DISPLAY"):
            print("Failed to initialize graphics display/No display found", file=sys.stderr)
            sys.exit(1)
        print("SimulationApp initialized successfully (mock).")

    def close(self):
        print("SimulationApp closed.")
