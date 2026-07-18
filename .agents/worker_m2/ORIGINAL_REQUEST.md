## 2026-07-11T11:41:40Z
Implement the WebRTC livestreaming configuration in `src/cinematic_city_drive.py`.

Specifically:
1. Under the `headless` check (if args.headless is True), configure the livestream port to 49100 using Carb settings, and enable the `"omni.services.streamclient.webrtc"` extension. This should occur right after initializing the `SimulationApp`.
2. To configure the port:
   ```python
   import carb
   carb.settings.get_settings().set("/app/livestream/port", 49100)
   ```
3. To enable the extension:
   ```python
   import omni.kit.app
   ext_manager = omni.kit.app.get_app().get_extension_manager()
   ext_manager.set_extension_enabled_immediate("omni.services.streamclient.webrtc", True)
   ```
4. Run the local test suite using the python interpreter inside `venv/Scripts/python.exe` to verify that all tests in `tests/e2e/test_webrtc_stream.py` pass.
   E.g., run:
   `venv\\Scripts\\python.exe -m pytest tests/e2e/test_webrtc_stream.py`
5. Document your implementation details, test commands run, and verification results in handoff.md under your working directory .agents/worker_m2.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
