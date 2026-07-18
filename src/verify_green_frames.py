import cv2
import glob
import sys
import numpy as np

def verify_green_frames():
    frames = glob.glob('/workspace/autonomous-berlin-pipeline/frames_small_city/*.jpg')
    if not frames:
        print("FAIL: No frames found in /workspace/autonomous-berlin-pipeline/frames_small_city/")
        sys.exit(1)
        
    print(f"Verifying {len(frames)} frames for green city buildings...")
    
    missing_green_count = 0
    for frame_path in frames:
        img = cv2.imread(frame_path)
        if img is None:
            print(f"Error reading {frame_path}")
            continue
            
        # Convert BGR to HSV to easily detect green
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define range of green color in HSV
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        
        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, lower_green, upper_green)
        green_pixel_count = cv2.countNonZero(mask)
        
        if green_pixel_count < 1000: # Ensure at least 1000 green pixels are visible
            print(f"FAIL: {frame_path} only has {green_pixel_count} green pixels. Scene might be blank or unlit.")
            missing_green_count += 1
            
    if missing_green_count > 0:
        print(f"Verification FAILED: {missing_green_count} frames failed the green pixel check.")
        sys.exit(1)
    
    print("Verification PASSED: All frames contain green city buildings.")
    sys.exit(0)

if __name__ == "__main__":
    verify_green_frames()
