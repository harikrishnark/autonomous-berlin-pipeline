## 2026-07-11T11:31:16Z

<USER_REQUEST>
Please explore the WebRTC streaming extensions in Isaac Sim on the remote VM.
1. Connect to the remote VM via SSH using host 157.157.221.29, port 24034, user root, and key C:\\Users\\aksha\\.ssh\\id_ed25519.
2. Run `/workspace/isaac_env/bin/python3 /workspace/autonomous-berlin-pipeline/src/list_exts.py` on the VM to see which extensions are available.
3. If list_registry_exts.py exists, also run it. Check if there are other extensions like `omni.kit.livestream.webrtc` or `omni.services.streamclient.webrtc` or similar.
4. Investigate how we can enable the WebRTC extension and configure it to use port 49100. (e.g., via carb.settings, command line arguments, or app.config settings).
5. Document your findings in handoff.md under your working directory .agents/explorer_m1.
6. Report back when complete.
</USER_REQUEST>
