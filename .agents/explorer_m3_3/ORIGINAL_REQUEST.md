# Original Request for explorer_m3_3

## Objective
Analyze the codebase and propose a remediation strategy to fix the Forensic Audit Integrity Violation in the E2E test suite.

## The Forensic Auditor's Verdict and Full Evidence Report
The Forensic Auditor reported an **INTEGRITY VIOLATION**:

```markdown
## Forensic Audit Report

**Work Product**: E2E Testing Suite (`tests/e2e/test_webrtc_stream.py`) and Mock Simulation Stack (`tests/mock_isaacsim/`)
**Profile**: General Project
**Verdict**: INTEGRITY VIOLATION

### Phase Results
- **Hardcoded output detection**: FAIL — The mock package `tests/mock_isaacsim/ultralytics/__init__.py` hardcodes the YOLO detection results. The mock `YOLO.__call__` method always returns a static bounding box for class 0 (person) at coordinates `[10, 350, 630, 470]` regardless of the frame contents. This bypasses real model logic and guarantees the `network_brain.py` socket server's output will always be `BRAKE` (since y2 = 470 > 400).
- **Facade detection**: FAIL — The `ultralytics` module inside `tests/mock_isaacsim/` is a facade implementation of the third-party YOLOv8 package. By prepending `tests/mock_isaacsim/` to the `PYTHONPATH`, the E2E tests intercept all `ultralytics` imports, bypassing the actual installed YOLOv8 package and the `yolov8n.pt` model weights. Additionally, `tests/mock_isaacsim/omni/isaac/sensor.py`'s `Camera.get_rgba()` returns a hardcoded blank image with a red rectangle.
- **Pre-populated artifact detection**: PASS — No pre-populated test results or fake verification logs exist in the repository that predated the run.
- **Build and run**: PASS — The E2E tests run successfully and all 40 test cases pass within ~13 seconds when running `venv\Scripts\pytest -v tests/e2e/test_webrtc_stream.py`.
- **Output verification**: FAIL — Because of the mock `ultralytics` facade, the test suite does not run the real YOLOv8 model. The latency throughput test `test_t4_perception_processing_throughput` benchmarks Python class instantiation in <1ms instead of benchmarking actual model inference (which takes ~75ms on CPU). Similarly, `test_t4_pipeline_full_lifecycle_run` passes even if a completely blank/empty frame is sent, because the mock YOLO always returns the hardcoded person box.
- **Dependency audit**: FAIL — The core AI perception layer (`ultralytics.YOLO`) is replaced by a dummy facade implementation, meaning the perception-control loop testing is not integrated with the actual target perception library.

---

### Evidence

#### 1. Hardcoded Mock YOLO Bounding Box (`tests/mock_isaacsim/ultralytics/__init__.py`)
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

#### 2. Hardcoded Mock Camera Image (`tests/mock_isaacsim/omni/isaac/sensor.py`)
```python
class Camera:
    def __init__(self, prim_path, position, frequency, resolution, orientation):
        self.resolution = resolution
    def initialize(self):
        pass
    def get_rgba(self):
        h, w = self.resolution[1], self.resolution[0]
        # Return a dummy image with a red rectangle (R=255, G=0, B=0, A=255)
        # this will trigger YOLO / perception module to output BRAKE command
        img = np.zeros((h, w, 4), dtype=np.uint8)
        img[350:470, 10:630, 0] = 255
        img[350:470, 10:630, 3] = 255
        return img
```

#### 3. Execution of Real YOLOv8 Model vs. Mocked YOLOv8 Model
An empirical test was run to verify if the real YOLOv8 model (which is installed in the local environment and uses `yolov8n.pt` weights) detects any object in the image sent by the client (a black frame with a red rectangle at `(10, 350)` to `(630, 470)`):

- **Real YOLOv8 output**:
  ```powershell
  venv\Scripts\python -c "import cv2, numpy as np; from ultralytics import YOLO; model = YOLO('yolov8n.pt'); img = np.zeros((480, 640, 3), dtype=np.uint8); cv2.rectangle(img, (10, 350), (630, 470), (0, 0, 255), -1); results = model(img, verbose=False); print([ (int(box.cls[0]), box.xyxy[0].tolist()) for r in results for box in r.boxes ])"
  []
  ```
  *Result*: The real model detects nothing (`[]`), which would cause `network_brain.py` to output `DRIVE`.

- **Mocked YOLOv8 output**:
  Always returns a detection of a person (class 0) at `[10, 350, 630, 470]`. This forces `network_brain.py` to output `BRAKE`, masking the fact that the actual AI model does not detect anything in the synthetic test frame.

- **Throughput Benchmark Bypass**:
  The real YOLOv8 inference takes **75.02ms** on CPU:
  ```powershell
  venv\Scripts\python -c "import time, cv2, numpy as np; from ultralytics import YOLO; model = YOLO('yolov8n.pt'); img = np.zeros((640, 480, 3), dtype=np.uint8); model(img, verbose=False); start = time.time(); n_iters = 30; [model(img, verbose=False) for _ in range(n_iters)]; end = time.time(); avg_ms = ((end - start) / n_iters) * 1000.0; print(f'AVG_TIME={avg_ms:.2f}ms')"
  AVG_TIME=75.02ms
  ```
  The mock model executes in **<0.1ms** because it bypasses all model loading and inference logic, fabricating the passing benchmark output.
```

## Remediated Strategy Requirements
1. The mock `ultralytics` package inside `tests/mock_isaacsim/` must be entirely removed or bypassed so the E2E tests run the actual installed `ultralytics` package and model inference using the real `yolov8n.pt` weights.
2. The mock Isaac Sim stack (`tests/mock_isaacsim/omni/`) may remain since running full Isaac Sim is not possible locally without hardware.
3. The E2E tests and mock simulation stack must be configured so that the mock camera `get_rgba()` returns an actual image that triggers real object/obstacle detections (e.g., returning `bus.jpg` contents or similar valid image data where the real YOLO model detects objects).
4. Benchmark tests (`test_t4_perception_processing_throughput`) and lifecycle tests (`test_t4_pipeline_full_lifecycle_run`) must use the real `ultralytics` library to run genuine inference and assert correct, non-hardcoded behavior and latencies.

## Tasks
1. Investigate the E2E test file (`tests/e2e/test_webrtc_stream.py`) and mock package (`tests/mock_isaacsim/`).
2. Design a concrete fix strategy showing how to integrate the real `ultralytics` package and make tests pass cleanly.
3. Write your analysis and handoff report in your folder.

## 2026-07-11T12:10:22Z
You are the explorer subagent (explorer_m3_3).
Your working directory is: c:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline\.agents\explorer_m3_3
Project workspace directory: c:\Users\aksha\OneDrive\Documents\self_driving\autonomous-berlin-pipeline

Your objective:
1. Recover your state by reading BRIEFING.md and ORIGINAL_REQUEST.md in your working directory.
2. Read the Forensic Auditor's full evidence report contained in ORIGINAL_REQUEST.md.
3. Investigate the codebase, in particular `tests/e2e/test_webrtc_stream.py` and the mock package `tests/mock_isaacsim/`.
4. Propose a clear remediation strategy showing how we can remove the mock `ultralytics` package, import and run the real `ultralytics` model, and modify the test/mock inputs (e.g. mock camera image returning `bus.jpg` or similar image that real YOLOv8 model detects objects in) to pass the tests.
5. Create a `progress.md` inside your directory to track progress.
6. Write a handoff report `handoff.md` in your directory, and send a message back to the orchestrator (conversation ID: c7e9a76d-bda6-4d3a-a1c4-0d890eb9bf89) once completed.
