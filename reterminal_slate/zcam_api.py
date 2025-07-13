import requests
import socket
CAM_IP = "10.98.33.1"

def rec_toggle(on):
    cmd = "start" if on else "stop"
    try:
        requests.get(
            f"http://{CAM_IP}/cgi-bin/zcmd?cmd=record&value={cmd}",
            timeout=1)
        return True
    except requests.Timeout:
        return False

def check_camera():
    try:
        # Try to open a socket connection to port 80
        sock = socket.create_connection((CAM_IP, 80), timeout=1)
        sock.close()
        return 'Live'
    except Exception:
        return 'Offline'
