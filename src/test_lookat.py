import omni.isaac.core.utils.rotations as rot
import numpy as np

cam_pos = np.array([-25.0, -25.0, 45.0])
target = np.array([-2.8, 0.0, 1.0])
up = np.array([0.0, 0.0, 1.0])

try:
    if hasattr(rot, 'lookat_to_quatf'):
        q = rot.lookat_to_quatf(cam_pos, target, up)
        print("lookat_to_quatf exists:", q)
    else:
        print("Functions in rot:")
        for name in dir(rot):
            if 'look' in name.lower() or 'quat' in name.lower():
                print(name)
except Exception as e:
    print("Error:", e)
