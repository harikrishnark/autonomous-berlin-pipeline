# Handoff Report - explorer_m3_3

## 1. Observation
- **Mock ultralytics Facade Interception**: 
  The file `tests/mock_isaacsim/ultralytics/__init__.py` contains a mock class `YOLO` that hardcodes class 0 (person) at `[10, 350, 630, 470]` for any input:
  ```python
  class YOLO:
      def __init__(self, model_path=None):
          pass
      def __call__(self, frame, verbose=False):
          class Box:
              def __init__(self):
                  self.cls = [0]  # person
                  self.xyxy = [[10, 350, 630, 470]]
          class Result:
              def __init__(self):
                  self.boxes = [Box()]
          return [Result()]
  ```
  The mock directory is added to `sys.path` (via `PYTHONPATH` prepend) in `tests/e2e/test_webrtc_stream.py` line 137:
  ```python
  env["PYTHONPATH"] = mock_isaacsim_path + os.pathsep + env.get("PYTHONPATH", "")
  ```
- **Dummy Mock Camera Image**: 
  The camera mock in `tests/mock_isaacsim/omni/isaac/sensor.py` generates a flat black frame with a red rectangle:
  ```python
      def get_rgba(self):
          h, w = self.resolution[1], self.resolution[0]
          # Return a dummy image with a red rectangle (R=255, G=0, B=0, A=255)
          # this will trigger YOLO / perception module to output BRAKE command
          img = np.zeros((h, w, 4), dtype=np.uint8)
          img[350:470, 10:630, 0] = 255
          img[350:470, 10:630, 3] = 255
          return img
  ```
- **Hardcoded E2E Test Client Image**: 
  The E2E lifecycle integration test `test_t4_pipeline_full_lifecycle_run` in `tests/e2e/test_webrtc_stream.py` constructs a similar black image with a red rectangle:
  ```python
      img = np.zeros((480, 640, 3), dtype=np.uint8)
      cv2.rectangle(img, (10, 350), (630, 470), (0, 0, 255), -1)
      _, encoded = cv2.imencode('.jpg', img)
      data = encoded.tobytes()
  ```
- **Real YOLOv8 Inference on Red Rectangle vs. bus.jpg**:
  - Running real YOLOv8 on the red rectangle image outputs `[]` (no detections), which would cause `network_brain.py` to output `DRIVE`, causing the E2E lifecycle test to fail.
  - Running real YOLOv8 on `bus.jpg` (both raw `1080x810` and resized to `640x480`) yields multiple class 0 (person) detections with bottom coordinates `y2 > 400` (e.g. `403.28` for resized), which naturally triggers the `BRAKE` command.

## 2. Logic Chain
1. Prepending `tests/mock_isaacsim` to `PYTHONPATH` causes python to find the mock `ultralytics` directory first. Deleting this directory will force Python to import the real `ultralytics` library installed in the `venv` site-packages.
2. Under the real `ultralytics` model, the red rectangle mockup yields `[]` detections, resulting in a `DRIVE` command. This will fail `test_t4_pipeline_full_lifecycle_run` which asserts `RESP=BRAKE`.
3. In contrast, the real `ultralytics` model run on `bus.jpg` resized to `640x480` detects a person with a bottom y-coordinate `y2 = 403.28 > 400`.
4. Therefore, modifying the mock camera `get_rgba()` and the E2E lifecycle client image input to load, resize, and send/return the `bus.jpg` image will trigger `BRAKE` natively under the real model.
5. Deleting the mock `ultralytics` package and modifying these inputs guarantees that the E2E tests pass while running genuine, un-mocked YOLOv8 perception inference.

## 3. Caveats
- We assume `bus.jpg` is always present in the repository root. Since it is committed to git, this holds true.
- We assume CPU performance is sufficient. Empirical checks show CPU average inference time is ~75.02ms, well within the 150.0ms threshold defined in `test_t4_perception_processing_throughput`.

## 4. Conclusion
To resolve the Forensic Audit Integrity Violation:
1. Delete the `tests/mock_isaacsim/ultralytics` directory entirely.
2. Replace `tests/mock_isaacsim/omni/isaac/sensor.py` with `proposed_sensor.py` which loads `bus.jpg` and returns it as an RGBA image resized to camera resolution.
3. Apply `proposed_test_webrtc_stream.patch` to `tests/e2e/test_webrtc_stream.py` to make the lifecycle integration test client send `bus.jpg` bytes.

## 5. Verification Method
1. Delete `tests/mock_isaacsim/ultralytics/` directory.
2. Apply changes in `proposed_sensor.py` and `proposed_test_webrtc_stream.patch`.
3. Run the E2E tests:
   ```powershell
   venv\Scripts\pytest -v tests/e2e/test_webrtc_stream.py
   ```
4. Confirm that all 40 tests pass successfully. Invalidation condition: any benchmark tests or lifecycle tests failing or raising import errors.
