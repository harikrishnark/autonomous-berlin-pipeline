# Project: WebRTC Streaming Enablement

## Architecture
- `src/cinematic_city_drive.py`: Headless Isaac Sim simulation script. Renders a cinematic drive of a Carter v1 robot in Rivermark City.
- WebRTC Livestreaming: Configured via Omniverse WebRTC extension (`omni.services.streamclient.webrtc` or similar) to broadcast viewport.
- SSH Tunneling: Binds remote signaling/media ports (TCP 49100, UDP 47998) to local ports for secure local browser viewing.
- Verification Suite: Checks for active listening on TCP 49100 and confirms non-crashing execution of the simulation script.

## Code Layout
- `src/cinematic_city_drive.py`: Target simulation script.
- `scripts/`: Verification scripts and helper tools.
- `tests/`: Feature and verification test cases.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | E2E Test Suite | Design opaque-box test cases for signaling server port and simulation stability, publishing `TEST_READY.md`. | None | DONE |
| 2 | WebRTC Integration | Update `src/cinematic_city_drive.py` to load and configure the WebRTC extension. | None | DONE |
| 3 | Final E2E Pass & Hardening | Run E2E tests, verify tunnel command, execute Tier 5 white-box coverage checks. | M1, M2 | IN_PROGRESS |

## Interface Contracts
- `src/cinematic_city_drive.py` CLI interface: Accepts `--headless` flag (should default to False or True as per original script, but needs to work headless).
- Signalling Server: Listens on port 49100.
