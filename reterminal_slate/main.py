import tkinter as tk
from markers import purple_mark, blue_mark, check_midi, midi_status
from zcam_api import rec_toggle, get_camera_status, get_video_format, get_camera_name, get_temperature, check_wifi_connection, get_storage_gb
from preview import launch_preview
from fkey_listener import FKeyListener
import time
import threading
import requests

# Globals for timer
recording_start_time = 0
is_recording = False
auto_mark_timer = None
clap_countdown_start = 0
clap_countdown_active = False

# Color and font constants matching wireframe
CLR_BG        = "#222"
CLR_TEXT      = "#ffffff"
CLR_MARK      = "#6a5acd"   # idle
CLR_REC_IDLE  = "#444444"
CLR_REC_ARM   = "#d04a4a"
CLR_PREV      = "#009688"
CLR_PREV_ON   = "#00695c"
CLR_COUNTER   = "#00e676"

FNT_BTN  = ("Helvetica", 36, "bold")
FNT_TIME = ("Roboto Mono", 64, "bold")
FNT_BAR  = ("Helvetica", 16)

# Button dimensions and positions from wireframe
BTN_W, BTN_H = 260, 110
MARK_X, REC_X, PREV_X, BTN_Y = 160, 510, 860, 260

root = tk.Tk()
root.geometry("1280x720")
root.configure(bg=CLR_BG)
root.attributes("-fullscreen", True)

# ── Status bar ──────────────────────────────────────────────────
status_bar = tk.Label(root, text="Initializing...", 
                     fg=CLR_TEXT, bg=CLR_BG, font=FNT_BAR, anchor="w")
status_bar.place(x=10, y=5, width=1260, height=30)

# ── Timer label ────────────────────────────────────────────────
timer_lbl = tk.Label(root, text="00:00", fg=CLR_COUNTER, bg=CLR_BG, font=FNT_TIME)
timer_lbl.place(x=0, y=50, width=1280, height=90)

# ── Clap countdown label ───────────────────────────────────────
countdown_lbl = tk.Label(root, text="", fg="#ff6600", bg=CLR_BG, font=("Roboto Mono", 48, "bold"))
countdown_lbl.place(x=950, y=150, width=300, height=80)

def format_status_bar(camera_data=None):
    """Format comprehensive status bar with all requested information"""
    try:
        # Get camera IP
        cam_ip = "10.98.33.1"
        
        # Get video format
        try:
            video_format = get_video_format()
        except:
            video_format = "N/A"
        
        # Get temperature
        try:
            temp = get_temperature()
            temp_str = f"{temp}°C" if temp and temp != "N/A" else "N/A"
        except:
            temp_str = "N/A"
            
        # Get white balance
        wb = "N/A"
        if camera_data and 'white_balance' in camera_data:
            wb = camera_data['white_balance']
        
        # Get ISO
        iso = "N/A"
        if camera_data and 'iso' in camera_data:
            iso = camera_data['iso']
        
        # Get battery percentage
        battery = "N/A"
        if camera_data and 'battery' in camera_data:
            battery = f"{camera_data['battery']}%"
        
        # Get storage space
        try:
            storage_gb = get_storage_gb()
            storage = f"{storage_gb}GB" if storage_gb else "N/A"
        except:
            storage = "N/A"
        
        # Check MIDI connection
        midi_conn = "MIDI ON" if midi_status == "Connected" else "MIDI OFF"
        
        # Check WiFi connection to camera
        try:
            wifi_conn = "WiFi ON" if check_wifi_connection() else "WiFi OFF"
        except:
            wifi_conn = "WiFi OFF"
        
        # Format comprehensive status line
        return f"IP:{cam_ip} • {video_format} • {temp_str} • WB:{wb} • ISO:{iso} • {storage} • {midi_conn} • {wifi_conn}"
        
    except Exception as e:
        return "Status: Error retrieving data"

def update_status():
    """Update status display every 5 seconds"""
    try:
        # Get camera status
        camera_status = get_camera_status()
        status_text = format_status_bar(camera_status)
        status_bar.config(text=status_text)
        
    except Exception as e:
        status_bar.config(text="Status: Connection Error")
    
    # Schedule next update
    root.after(5000, update_status)

def update_clock():
    """Update the timer/clock display and clap countdown"""
    global clap_countdown_active
    
    if is_recording and recording_start_time > 0:
        elapsed = int(time.time() - recording_start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        timer_lbl.config(text=timer_text, fg="#ff4444")
    else:
        current_time = time.strftime("%H:%M")
        timer_lbl.config(text=current_time, fg=CLR_COUNTER)
    
    # Handle clap countdown
    if clap_countdown_active and clap_countdown_start > 0:
        countdown_elapsed = time.time() - clap_countdown_start
        countdown_remaining = max(0, 15 - int(countdown_elapsed))
        
        if countdown_remaining > 0:
            countdown_lbl.config(text=f"CLAP IN\n{countdown_remaining}", fg="#ff6600")
        else:
            countdown_lbl.config(text="CLAP!", fg="#00ff00")
            # Hide countdown after 2 seconds
            if countdown_elapsed > 17:  # 15 seconds + 2 seconds showing "CLAP!"
                countdown_lbl.config(text="")
                clap_countdown_active = False
    else:
        countdown_lbl.config(text="")
    
    root.after(1000, update_clock)

def schedule_auto_mark():
    """Schedule automatic markers every 15 minutes"""
    global auto_mark_timer
    if is_recording:
        blue_mark()  # Send blue marker for auto marks
        auto_mark_timer = threading.Timer(900, schedule_auto_mark)  # 15 minutes
        auto_mark_timer.start()

def schedule_initial_clap():
    """Schedule initial clap marker 15 seconds after recording starts"""
    if is_recording:
        blue_mark()  # Send initial "clap" marker
        # Schedule first regular auto-marker 15 minutes after this clap
        global auto_mark_timer
        auto_mark_timer = threading.Timer(900, schedule_auto_mark)  # 15 minutes from clap
        auto_mark_timer.start()

def rec_toggle_cb():
    """Toggle recording state with proper button colors"""
    global is_recording, recording_start_time, auto_mark_timer, clap_countdown_start, clap_countdown_active
    
    try:
        if not is_recording:
            # Try to start recording
            start_url = f"http://10.98.33.1/ctrl/rec?action=start"
            response = requests.get(start_url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    # Start recording successful
                    is_recording = True
                    recording_start_time = time.time()
                    clap_countdown_start = time.time()
                    clap_countdown_active = True
                    btn_rec.config(bg=CLR_REC_ARM, text="STOP")
                    # Schedule initial clap marker after 15 seconds
                    threading.Timer(15, schedule_initial_clap).start()
                    print("DEBUG: Recording started - clap marker scheduled for 15 seconds")
                else:
                    btn_rec.config(bg="#ff8800")  # Orange for error
                    print("DEBUG: Recording start failed")
            else:
                btn_rec.config(bg="#ff8800")  # Orange for error
        else:
            # Try to stop recording
            stop_url = f"http://10.98.33.1/ctrl/rec?action=stop"
            response = requests.get(stop_url, timeout=3)
            if response.status_code == 200:
                # Stop recording
                is_recording = False
                recording_start_time = 0
                clap_countdown_active = False
                countdown_lbl.config(text="")
                btn_rec.config(bg=CLR_REC_IDLE, text="REC")
                if auto_mark_timer:
                    auto_mark_timer.cancel()
                print("DEBUG: Recording stopped")
            else:
                btn_rec.config(bg="#ff8800")  # Orange for error
    except Exception as e:
        btn_rec.config(bg="#ff8800")  # Orange for error
        print(f"Recording error: {e}")

def preview_toggle():
    """Launch Z CAM web interface in browser"""
    try:
        btn_prev.config(bg=CLR_PREV_ON)
        launch_preview()  # Launch Z CAM web interface
        # Reset button color after a moment
        root.after(2000, lambda: btn_prev.config(bg=CLR_PREV))
    except Exception as e:
        print(f"Preview error: {e}")

# ── Buttons row ────────────────────────────────────────────────
btn_mark = tk.Button(root, text="MARK", bg=CLR_MARK, fg=CLR_TEXT,
                     font=FNT_BTN, activebackground=CLR_MARK,
                     command=purple_mark)
btn_mark.place(x=MARK_X, y=BTN_Y, width=BTN_W, height=BTN_H)

btn_rec = tk.Button(root, text="REC", bg=CLR_REC_IDLE, fg=CLR_TEXT,
                    font=FNT_BTN, activebackground=CLR_REC_ARM,
                    command=rec_toggle_cb)
btn_rec.place(x=REC_X, y=BTN_Y, width=BTN_W, height=BTN_H)

btn_prev = tk.Button(root, text="PREVIEW", bg=CLR_PREV, fg=CLR_TEXT,
                     font=FNT_BTN, activebackground=CLR_PREV_ON,
                     command=preview_toggle)
btn_prev.place(x=PREV_X, y=BTN_Y, width=BTN_W, height=BTN_H)

# ── EXIT button ────────────────────────────────────────────────
btn_exit = tk.Button(root, text="EXIT", bg="#444", fg=CLR_TEXT,
                     font=("Helvetica", 24, "bold"), activebackground="#666",
                     command=lambda: root.destroy())
btn_exit.place(x=REC_X, y=BTN_Y+BTN_H+20, width=BTN_W, height=60)

# FKeyListener handler
def handle_fkey(key):
    if key == 'F1':
        # Launch the app (no-op if already running)
        pass
    elif key == 'F2':
        preview_toggle()
    elif key == 'F3':
        root.destroy()

fkey_listener = FKeyListener(handle_fkey)
fkey_listener.start()

update_status()
update_clock()
root.mainloop()

fkey_listener.stop()
