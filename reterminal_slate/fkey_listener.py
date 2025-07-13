import threading
import evdev
from evdev import InputDevice, categorize, ecodes

# You may need to adjust this path to match your reTerminal's F-key input device
FKEY_DEVICE = '/dev/input/event0'

class FKeyListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.running = True
        try:
            self.device = InputDevice(FKEY_DEVICE)
        except Exception as e:
            print(f"FKeyListener error: {e}")
            self.device = None

    def run(self):
        if not self.device:
            return
        for event in self.device.read_loop():
            if not self.running:
                break
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    if key_event.keycode == 'KEY_F2':
                        self.callback('F2')

    def stop(self):
        self.running = False

# Example usage:
# def handle_fkey(key):
#     print(f"Pressed: {key}")
# listener = FKeyListener(handle_fkey)
# listener.start()
# ...
# listener.stop()
