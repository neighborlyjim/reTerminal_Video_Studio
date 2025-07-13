import subprocess
import os

RTSP = "http://10.98.33.1/"  # Z CAM web UI

def get_browsers():
    """Get browser commands with current RTSP URL - prioritize modern browsers for Z CAM web UI"""
    return [
        ["chromium-browser", "--kiosk", "--new-window", "--disable-infobars", "--disable-extensions", RTSP],  # Chromium kiosk mode first
        ["chromium-browser", "--start-fullscreen", "--new-window", RTSP],  # Chromium fullscreen fallback
        ["firefox", "--kiosk", "--new-instance", RTSP],  # Firefox fullscreen kiosk mode
        ["firefox", "--fullscreen", RTSP],              # Firefox fullscreen fallback
        ["chromium-browser", RTSP],                     # Chromium regular fallback
        ["firefox", RTSP],                              # Firefox fallback without kiosk
        ["netsurf-gtk", RTSP],                          # Basic fallback
        ["xdg-open", RTSP],                             # System default
    ]

def kill_all():
    # Kill all supported browsers
    for browser in ["netsurf-gtk", "netsurf", "midori", "chromium-browser", "firefox"]:
        subprocess.call(["pkill", "-f", browser], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch_preview():
    print("DEBUG: launch_preview() called")
    kill_all()  # Always kill previous browser before launching
    
    # Set up environment for GUI applications
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    env['XAUTHORITY'] = '/home/jharris/.Xauthority'
    
    print(f"DEBUG: Environment DISPLAY={env.get('DISPLAY')}, XAUTHORITY={env.get('XAUTHORITY')}")
    print(f"DEBUG: Trying to open URL: {RTSP}")
    
    browsers = get_browsers()
    for browser_cmd in browsers:
        try:
            print(f"DEBUG: Attempting to launch: {' '.join(browser_cmd)}")
            # Run as user jharris if we're running as root
            if os.getuid() == 0:  # If running as root
                cmd = ['sudo', '-u', 'jharris'] + browser_cmd
                proc = subprocess.Popen(cmd, env=env)
            else:
                proc = subprocess.Popen(browser_cmd, env=env)
            print(f"DEBUG: Successfully launched: {' '.join(browser_cmd)} with PID {proc.pid}")
            return
        except Exception as e:
            print(f"DEBUG: Failed to launch {' '.join(browser_cmd)}: {e}")
    print("DEBUG: No supported browser found!")
