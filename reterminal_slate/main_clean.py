import tkinter as tk, threading, time
from markers import purple_mark, blue_mark, check_midi
from zcam_api import rec_toggle, check_camera
import preview
from fkey_listener import FKeyListener

# --- Constants ---
BG_COLOR = "#222"
MARK_IDLE = "#6a5acd"
MARK_ACTIVE = "#9370db"
REC_IDLE = "#444"
REC_ACTIVE = "#d04a4a"
REC_ERROR = "#ff9100"
PREV_IDLE = "#009688"
PREV_ACTIVE = "#00695c"
TIMER_COLOR = "#00e676"
BTN_W, BTN_H = 260, 110
BTN_Y = 260
BTN_SPACING = 350
MARK_X = 160
REC_X = MARK_X + BTN_SPACING
PREV_X = REC_X + BTN_SPACING

root = tk.Tk()
root.attributes('-fullscreen', True)
root.geometry("1280x720")
root.configure(bg=BG_COLOR)
root.focus_force()  # Force focus to make fullscreen work properly
root.lift()  # Bring window to front

# Ensure fullscreen after window is created
def ensure_fullscreen():
    root.attributes('-fullscreen', True)
    root.focus_force()
    root.lift()

root.after(100, ensure_fullscreen)  # Apply fullscreen after 100ms

# --- State ---
auto_on = False
rec_on = False
start_ts = None
scheduler_id = None
preview_on = False

# --- Timer logic ---
def schedule_tick():
    global scheduler_id
    if not auto_on: return
    blue_mark()
    scheduler_id = root.after(5*60*1000, schedule_tick)

def toggle_timer(arm):
    global auto_on, start_ts, scheduler_id
    auto_on = arm
    if auto_on:
        start_ts = time.time()
        schedule_tick()
        timer_lbl.config(text="00:00")
    else:
        if scheduler_id:
            root.after_cancel(scheduler_id)
            scheduler_id = None
        timer_lbl.config(text="00:00")

# --- UI ---
timer_lbl = tk.Label(root, text="00:00", fg=TIMER_COLOR, bg=BG_COLOR, font=("Roboto Mono",64,"bold"), anchor="center")
timer_lbl.place(x=0, y=50, width=1280, height=90)

status_lbl = tk.Label(root, text="", fg="#fff", bg=BG_COLOR, font=("Helvetica",18,"bold"))
status_lbl.place(x=0, y=10, width=1280, height=30)

def update_status():
    midi = check_midi()
    cam = check_camera()
    status_lbl.config(text=f"MIDI: {midi}   |   Camera: {cam}")
    root.after(2000, update_status)

def update_clock():
    if auto_on and start_ts:
        dt = int(time.time() - start_ts)
        mm, ss = divmod(dt, 60)
        timer_lbl.config(text=f"{mm:02}:{ss:02}")
    root.after(500, update_clock)

# --- Button handlers ---
def mark_flash():
    btn_mark.config(bg=MARK_ACTIVE, activebackground=MARK_ACTIVE)
    root.after(250, lambda: btn_mark.config(bg=MARK_IDLE, activebackground=MARK_ACTIVE))

def rec_flash(color):
    btn_rec.config(bg=color, activebackground=color)
    root.after(250, lambda: btn_rec.config(bg=REC_ACTIVE if rec_on else REC_IDLE, activebackground=REC_ACTIVE if rec_on else REC_IDLE))

def mark_cb():
    purple_mark()
    mark_flash()

def rec_cb():
    global rec_on
    rec_on = not rec_on
    if rec_on:
        # Start recording, arm timer
        print("DEBUG: Attempting to start recording...")
        ok = rec_toggle(True)
        if ok:
            btn_rec.config(bg=REC_ACTIVE, activebackground=REC_ACTIVE)
            toggle_timer(True)
            blue_mark() # Immediate blue tick
            print("DEBUG: Recording started successfully")
        else:
            rec_on = False  # Reset state on failure
            rec_flash(REC_ERROR)
            print("DEBUG: Failed to start recording")
    else:
        # Stop recording, disarm timer
        print("DEBUG: Attempting to stop recording...")
        ok = rec_toggle(False)
        btn_rec.config(bg=REC_IDLE, activebackground=REC_IDLE)
        toggle_timer(False)
        if not ok:
            rec_flash(REC_ERROR)
            print("DEBUG: Failed to stop recording")
        else:
            print("DEBUG: Recording stopped successfully")

def preview_cb():
    global preview_on
    preview_on = not preview_on
    if preview_on:
        print("DEBUG: Launching preview...")
        preview.launch_preview()
        btn_prev.config(bg=PREV_ACTIVE, activebackground=PREV_ACTIVE)
        back_btn.place(x=PREV_X, y=BTN_Y+BTN_H+40, width=BTN_W, height=BTN_H)
    else:
        print("DEBUG: Killing preview...")
        preview.kill_all()
        btn_prev.config(bg=PREV_IDLE, activebackground=PREV_ACTIVE)
        back_btn.place_forget()

# --- Create UI Elements ---
btn_mark = tk.Button(root, text="MARK", bg=MARK_IDLE, fg="#fff", font=("Helvetica",36,"bold"), 
                     activebackground=MARK_ACTIVE, activeforeground="#fff", command=mark_cb)
btn_rec  = tk.Button(root, text="REC",  bg=REC_IDLE,  fg="#fff", font=("Helvetica",36,"bold"),
                     activebackground=REC_IDLE, activeforeground="#fff", command=rec_cb)
btn_prev = tk.Button(root, text="PREVIEW", bg=PREV_IDLE, fg="#fff", font=("Helvetica",36,"bold"),
                     activebackground=PREV_ACTIVE, activeforeground="#fff", command=preview_cb)
exit_btn = tk.Button(root, text="EXIT", bg="#ff6b6b", fg="#fff", font=("Helvetica",28,"bold"), 
                     activebackground="#ff8a80", activeforeground="#fff", command=root.destroy)

btn_mark.place(x=MARK_X, y=BTN_Y, width=BTN_W, height=BTN_H)
btn_rec.place(x=REC_X, y=BTN_Y, width=BTN_W, height=BTN_H)
btn_prev.place(x=PREV_X, y=BTN_Y, width=BTN_W, height=BTN_H)
exit_btn.place(x=REC_X, y=BTN_Y+BTN_H+40, width=BTN_W, height=BTN_H)

back_btn = tk.Button(root, text="BACK", bg="#444", fg="#fff", font=("Helvetica",28,"bold"), 
                     activebackground="#666", activeforeground="#fff", command=lambda: preview_cb())
# Initially hidden
back_btn.place_forget()

# FKeyListener handler
def handle_fkey(key):
    if key == 'F1':
        # Launch the app (no-op if already running)
        pass
    elif key == 'F2':
        preview_cb()
    elif key == 'F3':
        root.destroy()

fkey_listener = FKeyListener(handle_fkey)
fkey_listener.start()

update_status()
update_clock()
root.mainloop()

fkey_listener.stop()
