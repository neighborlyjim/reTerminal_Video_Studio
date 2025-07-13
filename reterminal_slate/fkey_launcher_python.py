#!/usr/bin/env python3
"""
F-key listener and app launcher for reTerminal using evdev
Requires: python3-evdev (sudo apt-get install python3-evdev)
"""

import os
import sys
import subprocess
import time
from evdev import InputDevice, categorize, ecodes

# Configuration
FKEY_DEVICE = "/dev/input/event0"
APP_CMD = ["/home/jharris/reterminal_slate_venv/bin/python", 
           "/home/jharris/reTerminal_Video_Studio/reterminal_slate/main.py"]

# Key mappings from your evtest output
KEY_CODES = {
    30: "F1",    # KEY_A
    31: "F2",    # KEY_S  
    32: "F3",    # KEY_D
    33: "GREEN", # KEY_F
}

def launch_app():
    """Launch the main app"""
    try:
        print("F1 (KEY_A) detected, launching app!")
        # Set environment variables for GUI
        env = os.environ.copy()
        env['DISPLAY'] = ':0'
        env['XAUTHORITY'] = '/home/jharris/.Xauthority'
        subprocess.Popen(APP_CMD, env=env)
        time.sleep(1)  # Prevent multiple launches
    except Exception as e:
        print(f"Error launching app: {e}")

def handle_f2():
    """Handle F2 action"""
    print("F2 (KEY_S) detected!")
    # Add your F2 action here

def handle_f3():
    """Handle F3 action"""
    print("F3 (KEY_D) detected!")
    # Add your F3 action here

def handle_green():
    """Handle Green button action"""
    print("Green button (KEY_F) detected!")
    # Add your green button action here

def main():
    try:
        # Open the input device with exclusive access
        device = InputDevice(FKEY_DEVICE)
        device.grab()  # Grab device exclusively to prevent desktop from seeing events
        print(f"Listening for F-key events on {device.name} ({FKEY_DEVICE})")
        print("Device grabbed exclusively - desktop won't see F-key presses")
        print("Press Ctrl+C to exit")
        
        # Listen for events
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:  # Key press (not release)
                    if event.code in KEY_CODES:
                        key_name = KEY_CODES[event.code]
                        print(f"DEBUG: {key_name} pressed (code {event.code})")
                        
                        # Execute actions
                        if event.code == 30:  # F1 (KEY_A)
                            launch_app()
                        elif event.code == 31:  # F2 (KEY_S)
                            handle_f2()
                        elif event.code == 32:  # F3 (KEY_D)
                            handle_f3()
                        elif event.code == 33:  # Green (KEY_F)
                            handle_green()
                            
    except PermissionError:
        print(f"Permission denied accessing {FKEY_DEVICE}")
        print("Run this script with sudo:")
        print(f"sudo {sys.argv[0]}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Device {FKEY_DEVICE} not found")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        if 'device' in locals():
            device.ungrab()  # Release device
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if 'device' in locals():
            device.ungrab()  # Release device
        sys.exit(1)

if __name__ == "__main__":
    main()
