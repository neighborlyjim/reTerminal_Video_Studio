import requests
import socket
import json
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

def get_camera_status():
    """Get detailed camera status including battery, ISO, white balance, etc."""
    status_data = {}
    
    # Define the status keys we want to query (only keys that actually work)
    status_keys = {
        'battery': 'battery',
        'iso': 'iso',
        'wb': 'white_balance',
        'shutter': 'shutter',
        'resolution': 'resolution'
    }
    
    try:
        for key, display_name in status_keys.items():
            url = f"http://{CAM_IP}/ctrl/get?k={key}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data.get('code') == 0:  # Success
                    status_data[display_name] = data.get('value', 'N/A')
                else:
                    status_data[display_name] = 'N/A'
            else:
                status_data[display_name] = 'N/A'
        
        return status_data if status_data else None
        
    except Exception as e:
        print(f"DEBUG: Status request failed: {e}")
        return None

def check_camera():
    try:
        # Try to open a socket connection to port 80
        sock = socket.create_connection((CAM_IP, 80), timeout=1)
        sock.close()
        return 'Live'
    except Exception:
        return 'Offline'

def rec_toggle():
    """Toggle recording state - simplified version that checks current state"""
    try:
        # First check if we're currently recording by trying to start
        start_url = f"http://{CAM_IP}/ctrl/rec?action=start"
        response = requests.get(start_url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                print("DEBUG: Recording started")
                return True
            else:
                # If start failed, try stop (we're probably already recording)
                stop_url = f"http://{CAM_IP}/ctrl/rec?action=stop"
                stop_response = requests.get(stop_url, timeout=3)
                if stop_response.status_code == 200:
                    print("DEBUG: Recording stopped")
                    return True
        
        return False
    except Exception as e:
        print(f"DEBUG: Recording toggle failed: {e}")
        return False

def get_card_free_space():
    """Get storage card free space in GB using the msg field"""
    try:
        url = f"http://{CAM_IP}/ctrl/card?action=query_free"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                # Z CAM returns storage in 'msg' field as MB
                free_mb = data.get('msg', 0)
                if isinstance(free_mb, (int, float)):
                    free_gb = round(free_mb / 1024, 1)
                    return free_gb
    except Exception as e:
        print(f"DEBUG: Storage query failed: {e}")
    return None

def get_temperature():
    """Get camera temperature"""
    try:
        url = f"http://{CAM_IP}/ctrl/temperature"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                return data.get('temp', 'N/A')
    except Exception as e:
        print(f"DEBUG: Temperature query failed: {e}")
    return None

def get_wifi_signal():
    """Get WiFi signal strength"""
    try:
        url = f"http://{CAM_IP}/ctrl/wifi_ctrl?action=query"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                # This would parse actual signal strength from the response
                # For now, return a placeholder
                return "−48 dBm"
    except Exception as e:
        print(f"DEBUG: WiFi query failed: {e}")
    return "N/A"

def get_video_format():
    """Get current video format/resolution"""
    try:
        url = f"http://{CAM_IP}/ctrl/get?k=movfmt"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                return data.get('value', 'N/A')
    except Exception as e:
        print(f"DEBUG: Video format query failed: {e}")
    return "N/A"

def get_camera_name():
    """Get camera name/model from info endpoint"""
    try:
        url = f"http://{CAM_IP}/ctrl/info"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                return data.get('msg', 'Z CAM')
    except Exception as e:
        print(f"DEBUG: Camera info query failed: {e}")
    return "Z CAM"

def get_storage_gb():
    """Get storage card free space in GB using the msg field"""
    try:
        url = f"http://{CAM_IP}/ctrl/card?action=query_free"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                # Z CAM returns storage in 'msg' field as MB
                free_mb = data.get('msg', 0)
                if isinstance(free_mb, (int, float)):
                    free_gb = round(free_mb / 1024, 1)
                    return free_gb
    except Exception as e:
        print(f"DEBUG: Storage query failed: {e}")
    return None

def check_wifi_connection():
    """Check if WiFi is connected to Z CAM"""
    try:
        # Test connectivity to Z CAM
        response = requests.get(f"http://{CAM_IP}/ctrl/get?k=battery", timeout=2)
        return response.status_code == 200
    except:
        return False
