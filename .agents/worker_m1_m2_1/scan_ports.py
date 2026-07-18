import socket
import concurrent.futures
import sys

ip = '157.157.221.29'
open_ports = []

def scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is OPEN", flush=True)
            open_ports.append(port)
        s.close()
    except Exception:
        pass

# Scan common RunPod ports: 10000 to 32000
print("Starting port scan...", flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
    executor.map(scan, range(10000, 32000))

print(f"Finished scan. Open ports: {open_ports}", flush=True)
