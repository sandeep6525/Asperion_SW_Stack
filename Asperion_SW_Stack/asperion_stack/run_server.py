"""
Asperion Enterprise OS - Server Runner
"""
import uvicorn
import os
import sys
import socket
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def find_available_port(preferred_port: int = 8080) -> int:
    for p in [preferred_port, 8080, 8050, 8888, 5000, 3000]:
        try:
            s = socket.socket()
            s.bind(('127.0.0.1', p))
            s.close()
            return p
        except Exception:
            continue
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p

if __name__ == "__main__":
    env_port = int(os.environ.get("PORT", 8080))
    port = find_available_port(env_port)
    print(f"\n=======================================================")
    print(f" ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED")
    print(f" Enterprise Operating System Web Server")
    print(f" Web UI:     http://127.0.0.1:{port}")
    print(f" OpenAPI:    http://127.0.0.1:{port}/docs")
    print(f" ReDoc:      http://127.0.0.1:{port}/redoc")
    print(f"=======================================================\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
