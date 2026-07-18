import os
import cv2
import numpy as np

class Camera:
    def __init__(self, prim_path, position, frequency, resolution, orientation):
        self.resolution = resolution
    def initialize(self):
        pass
    def get_rgba(self):
        h, w = self.resolution[1], self.resolution[0]
        
        # Search for bus.jpg in the workspace
        possible_paths = [
            "bus.jpg",
            "/workspace/autonomous-berlin-pipeline/bus.jpg",
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "bus.jpg"),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bus.jpg")
        ]
        
        img_bgr = None
        for p in possible_paths:
            p_abs = os.path.abspath(p)
            if os.path.exists(p_abs):
                img_bgr = cv2.imread(p_abs)
                if img_bgr is not None:
                    break
                    
        if img_bgr is None:
            # Fallback to the original red rectangle dummy if bus.jpg is missing
            img = np.zeros((h, w, 4), dtype=np.uint8)
            img[350:470, 10:630, 0] = 255
            img[350:470, 10:630, 3] = 255
            return img

        # Resize the BGR image to the camera resolution (w, h)
        img_resized = cv2.resize(img_bgr, (w, h))
        # Convert BGR to RGBA
        img_rgba = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGBA)
        return img_rgba
