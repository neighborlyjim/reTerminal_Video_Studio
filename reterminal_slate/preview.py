import subprocess
import os

RTSP = "http://10.98.33.1/"  # Z CAM web UI

browser_cmd = [
    'midori', RTSP
]

browser_proc = None

def launch_preview():
    global browser_proc
    if browser_proc is None:
        try:
            browser_proc = subprocess.Popen(browser_cmd)
        except Exception:
            subprocess.Popen(['xdg-open', RTSP])

def kill_all():
    subprocess.call(['pkill', '-f', 'midori'])
    subprocess.call(['pkill', '-f', 'python'])
    global browser_proc
    browser_proc = None
