import os
import cv2
from ultralytics import YOLO

def verify_objects_in_frames(frames_dir):
    print(f"Verifying frames in {frames_dir} using YOLOv8...")
    
    if not os.path.exists(frames_dir):
        print(f"ERROR: Directory {frames_dir} does not exist.")
        return False
        
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    
    if not frame_files:
        print("ERROR: No frame files found.")
        return False

    try:
        model = YOLO('/workspace/autonomous-berlin-pipeline/yolov8n.pt')
    except Exception as e:
        print(f"ERROR: Could not load YOLOv8 model. Exception: {e}")
        return False

    # Check every 30th frame to save time (1 frame per second for 90 seconds = 90 frames)
    frames_to_check = frame_files[::30]
    failed_frames = 0
    total_cars_detected = 0

    for f in frames_to_check:
        img_path = os.path.join(frames_dir, f)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"FAIL: Could not read {img_path}")
            failed_frames += 1
            continue
            
        results = model(img, verbose=False)
        
        # Count the number of cars detected in this frame
        cars_in_frame = 0
        for r in results:
            for c in r.boxes.cls:
                if int(c) == 2:  # class 2 is 'car' in COCO
                    cars_in_frame += 1
                    
        total_cars_detected += cars_in_frame
        
        # If it's just a grey screen, it will detect 0 cars.
        if cars_in_frame == 0:
            print(f"FAIL: YOLOv8 detected 0 cars in {img_path}. Scene might be blank or shaders failed.")
            failed_frames += 1
            
    if total_cars_detected == 0 or failed_frames > 0:
        print(f"Verification FAILED: {failed_frames} out of {len(frames_to_check)} sampled frames failed the YOLO object check.")
        return False
        
    print(f"Verification PASSED: YOLOv8 detected a total of {total_cars_detected} cars across {len(frames_to_check)} sampled frames.")
    return True

if __name__ == "__main__":
    frames_dir = "/workspace/autonomous-berlin-pipeline/frames_small_city"
    success = verify_objects_in_frames(frames_dir)
    if not success:
        import sys
        sys.exit(1)
