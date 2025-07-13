import requests
import socket
CAM_IP = "10.98.33.1"

def rec_toggle(on):
    action = "start" if on else "stop"
    url = f"http://{CAM_IP}/ctrl/rec?action={action}"
    try:
        print(f"DEBUG: Sending request to {url}")
        response = requests.get(url, timeout=3)
        print(f"DEBUG: Response status: {response.status_code}")
        print(f"DEBUG: Response text: {response.text}")
        return response.status_code == 200
    except requests.Timeout:
        print("DEBUG: Request timed out")
        return False
    except Exception as e:
        print(f"DEBUG: Request failed: {e}")
        return False

def check_camera():
    try:
        # Try to open a socket connection to port 80
        sock = socket.create_connection((CAM_IP, 80), timeout=1)
        sock.close()
        return 'Live'
    except Exception:
        return 'Offline'
