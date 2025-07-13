import evdev
import subprocess
import threading

# You may need to adjust this path to match your reTerminal's F-key input device
FKEY_DEVICE = '/dev/input/event0'
APP_CMD = ['/home/jharris/reterminal_slate_venv/bin/python', '/home/jharris/reTerminal_Video_Studio/reterminal_slate/main.py']

class FKeyLauncher(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        try:
            self.device = evdev.InputDevice(FKEY_DEVICE)
        except Exception as e:
            print(f"FKeyLauncher error: {e}")
            self.device = None

    def run(self):
        if not self.device:
            return
        for event in self.device.read_loop():
            if not self.running:
                break
            if event.type == evdev.ecodes.EV_KEY:
                key_event = evdev.categorize(event)
                if key_event.keystate == key_event.key_down:
                    if key_event.keycode == 'KEY_F1':
                        subprocess.Popen(APP_CMD)

    def stop(self):
        self.running = False

if __name__ == '__main__':
    launcher = FKeyLauncher()
    launcher.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        launcher.stop()
