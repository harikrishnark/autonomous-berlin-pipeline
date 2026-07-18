# Scope: E2E Testing Track

## Architecture
- Opaque-box requirement-driven test framework.
- Independent of implementation internals.
- Verification targets:
  - Port 49100 listening for WebRTC signaling server.
  - Headless execution of cinematic_city_drive.py without crashes/segfaults.
  - SSH Tunneling command mapping ports (TCP 49100, UDP 47998) without error.
- Test runner and script locations (under `tests/e2e/`).

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Exploration & Design | Check repo layout, verify VM connectivity, write TEST_INFRA.md | None | DONE |
| 2 | Implementation | Implement test runner and test cases (Tiers 1-4, min 38 cases) | M1 | DONE |
| 3 | Review & Verification | Run the E2E tests, verify functionality, handle any failures | M2 | DONE |
| 4 | Final Validation | Forensic audit of test code, write TEST_READY.md | M3 | DONE |

## Interface Contracts
- E2E Test Suite command: to be defined in Milestone 1.
- Outputs must conform to WebRTC/Simulation requirements.
