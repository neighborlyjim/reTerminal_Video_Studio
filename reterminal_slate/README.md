# reTerminal Podcast Slate

A professional broadcast control interface for the Seeed reTerminal, designed for podcast and video production workflows. Features hardware button automation, Z CAM integration, and MIDI control.

## 🎯 Features

### 📺 Professional Broadcast Interface
- **Three-button layout**: MARK, REC, PREVIEW optimized for landscape orientation
- **Fullscreen kiosk mode** with 1280x720 resolution
- **Real-time timer** with recording synchronization
- **Status monitoring** for MIDI and camera connectivity

### 🎛️ Hardware Integration
- **F-key automation** via systemd service (F1 launch, F3 close preview)
- **Exclusive hardware access** prevents desktop interference
- **Z CAM recording control** via HTTP API
- **MIDI marker integration** for post-production workflow

### 📹 Camera Control
- **Start/stop recording** on Z CAM E2 series cameras
- **Live status monitoring** (camera online/offline detection)
- **Web interface preview** in fullscreen Chromium kiosk mode
- **Browser automation** with multiple fallback options

## 🚀 Quick Start

### Hardware Button Controls
- **F1**: Launch podcast slate app in fullscreen
- **F2**: Toggle preview window (Z CAM web interface)
- **F3**: Close preview window
- **Green button**: Reserved for future expansion

### Application Controls
- **MARK**: Send purple MIDI marker (manual chapter mark)
- **REC**: Start/stop Z CAM recording with timer sync
- **PREVIEW**: Open Z CAM web interface in browser
- **EXIT**: Close application

## ⚙️ Installation

### Prerequisites
```bash
sudo apt-get update
sudo apt-get install python3-evdev python3-requests chromium-browser
```

### Python Dependencies
```bash
cd /home/jharris/reTerminal_Video_Studio/reterminal_slate
pip install -r requirements.txt  # mido, python-rtmidi, requests
```

### Service Installation
```bash
# Copy service file to systemd
sudo cp fkey_launcher.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fkey_launcher.service
sudo systemctl start fkey_launcher.service
```

## 🔧 Configuration

### Network Setup
Update `zcam_api.py` with your Z CAM IP address:
```python
CAM_IP = "10.98.33.1"  # Change to your camera's IP
```

### MIDI Configuration
MIDI ports are auto-detected. Modify `markers.py` for specific routing:
```python
# Available MIDI output ports will be listed on startup
```

### Hardware Button Mapping
Hardware buttons are mapped in `fkey_launcher_python.py`:
```python
KEY_CODES = {
    30: "F1",    # KEY_A - Launch app
    31: "F2",    # KEY_S - Toggle preview  
    32: "F3",    # KEY_D - Close preview
    33: "GREEN", # KEY_F - Custom action
}
```

## 📁 Project Structure

```
reterminal_slate/
├── main.py                    # Main application UI
├── fkey_launcher_python.py    # Hardware button listener
├── fkey_launcher.service      # Systemd service configuration
├── markers.py                 # MIDI marker functions
├── zcam_api.py               # Z CAM HTTP API interface
├── preview.py                # Browser automation for camera preview
├── fkey_listener.py          # F-key event handler
└── reterminal_slate_addons.md # Enhancement roadmap
```

## 🔄 Workflow Integration

### Recording Session
1. **F1** launches the podcast slate interface
2. **MARK** sends chapter markers during recording
3. **REC** starts Z CAM recording and timer
4. **PREVIEW** monitors camera feed in real-time
5. **F3** quickly closes preview when needed
6. Timer tracks recording duration with 5-minute auto-markers

### Post-Production
- MIDI markers exported to DAW timeline
- Z CAM recordings automatically timestamped
- Manual markers distinguish talking points from auto-chapters

## 🛠️ API Endpoints

### Z CAM Control
```bash
# Start recording
GET http://10.98.33.1/ctrl/rec?action=start

# Stop recording  
GET http://10.98.33.1/ctrl/rec?action=stop

# Camera info (for status monitoring)
GET http://10.98.33.1/ctrl/info
```

### MIDI Integration
- **Purple markers**: Manual chapter marks (button press)
- **Blue markers**: Automatic interval marks (5-minute timer)
- **Output format**: Standard MIDI Time Code (MTC)

## 🔍 Troubleshooting

### Hardware Buttons Not Working
```bash
# Check service status
sudo systemctl status fkey_launcher.service

# View logs
sudo journalctl -u fkey_launcher.service -f

# Test device access
sudo evtest /dev/input/event0
```

### Camera Connection Issues
```bash
# Test camera connectivity
ping 10.98.33.1

# Test API manually
curl "http://10.98.33.1/ctrl/rec?action=start"
```

### Display Problems
```bash
# Launch with proper environment
DISPLAY=:0 XAUTHORITY=/home/jharris/.Xauthority python3 main.py
```

### Browser Preview Issues
```bash
# Check available browsers
which chromium-browser firefox netsurf-gtk

# Test browser manually
chromium-browser --kiosk http://10.98.33.1/
```

## 🚦 Status Indicators

### Button Colors
- **MARK**: Purple (idle) → Bright purple (active flash)
- **REC**: Gray (idle) → Red (recording) → Orange (error)
- **PREVIEW**: Teal (idle) → Dark teal (active)

### Status Bar
- **MIDI**: Connected/Disconnected status
- **Camera**: Live/Offline connection status

## 📈 Enhancement Roadmap

See `reterminal_slate_addons.md` for planned features:
- Enhanced status monitoring (Wi-Fi, storage, battery)
- RGB LED indicators
- Foot-switch integration
- Automatic backup workflows
- Advanced MIDI features

## 🔧 Development

### Testing Changes
```bash
# Kill existing app
sudo pkill -f main.py

# Launch with debug output
DISPLAY=:0 XAUTHORITY=/home/jharris/.Xauthority python3 main.py
```

### Service Management
```bash
# Restart hardware button service
sudo systemctl restart fkey_launcher.service

# Disable for development
sudo systemctl stop fkey_launcher.service
```

## 📄 License

MIT License - Professional broadcast control for content creators.

## 🔗 Links

- [Z CAM API Documentation](https://www.z-cam.com/)
- [Seeed reTerminal Hardware](https://wiki.seeedstudio.com/reTerminal/)
- [MIDI Technical Standard](https://www.midi.org/)
- [GitHub Repository](https://github.com/neighborlyjim/reTerminal_Video_Studio)
