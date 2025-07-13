# reTerminal Podcast Slate

A professional broadcast control interface for the Seeed reTerminal, designed for podcast and video production workflows. Features hardware button automation, Z CAM integration, MIDI control, and comprehensive real-time status monitoring.

## 📋 Quick Navigation

- [Latest Enhancements](#-latest-enhancements) - New enhanced status bar features
- [Quick Start](#-quick-start) - Get up and running immediately  
- [Installation](#️-installation) - Prerequisites and setup
- [Configuration](#-configuration) - Network setup and customization
- [API Endpoints](#️-api-endpoints) - Z CAM integration reference
- [Troubleshooting](#-troubleshooting) - Common issues and solutions
- [Documentation Links](#-documentation-links) - Additional references

## ✨ Latest Enhancements

**Enhanced Status Bar** - Now displays comprehensive real-time camera and system information:
- **Camera Details**: IP address, video format, temperature monitoring
- **Camera Settings**: Current ISO, white balance settings
- **System Status**: Storage space, MIDI connection, WiFi connectivity
- **Real-time Updates**: 5-second refresh cycle with graceful error handling

> **📖 Details:** See [Enhanced Status Bar Documentation](ENHANCED_STATUS_SUMMARY.md) for complete implementation information.

## 🎯 Features

### 📺 Professional Broadcast Interface
- **Three-button layout**: MARK, REC, PREVIEW optimized for landscape orientation
- **Fullscreen kiosk mode** with 1280x720 resolution
- **Real-time timer** with recording synchronization
- **Enhanced status monitoring**: IP address, video format, temperature, white balance, ISO, storage, MIDI and WiFi connectivity
- **Live status updates** every 5 seconds with comprehensive camera information

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
- **PREVIEW**: Open Z CAM web interface in external browser
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

### Network Setup for Z CAM Integration

#### reTerminal WiFi Connection
Connect your reTerminal to the Z CAM's WiFi network for camera control:

1. **Connect to Z CAM WiFi**:
   ```bash
   # Z CAM creates an access point when in WiFi mode
   SSID: ZCAM_xxxx (where xxxx is camera serial)
   Password: 12345678 (default)
   ```

2. **Verify Connection**:
   ```bash
   # Test camera connectivity
   ping 10.98.33.1
   
   # Test camera API
   curl "http://10.98.33.1/ctrl/get?k=battery"
   ```

#### Development & Troubleshooting
For development work, maintain a wired ethernet connection to your reTerminal:

1. **SSH over Ethernet** (recommended for development):
   ```bash
   # Connect via wired network for stable development access
   ssh jharris@<reterminal-ethernet-ip>
   
   # While reTerminal WiFi connects to Z CAM for camera control
   ```

2. **Network Configuration**:
   ```bash
   # Check network interfaces
   ip addr show
   
   # WiFi (wlan0): Connected to Z CAM network (10.98.33.x)
   # Ethernet (eth0): Connected to development network
   ```

3. **Troubleshooting Network Issues**:
   ```bash
   # Check Z CAM connection
   wget -qO- "http://10.98.33.1/ctrl/get?k=battery" | python3 -m json.tool
   
   # Test different Z CAM endpoints
   curl -s "http://10.98.33.1/ctrl/rec?action=start"
   ```

### Camera IP Configuration
Update `zcam_api.py` with your Z CAM IP address:
```python
CAM_IP = "10.98.33.1"  # Default Z CAM WiFi IP
# Change if using different network configuration
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
├── main.py                      # Main application UI with enhanced status bar
├── fkey_launcher_python.py      # Hardware button listener (systemd service)
├── fkey_launcher.service        # Systemd service configuration
├── markers.py                   # MIDI marker functions for RODECaster Pro
├── zcam_api.py                  # Z CAM HTTP API interface with comprehensive status
├── preview.py                   # Browser automation for camera preview
├── fkey_listener.py             # F-key event handler
├── README.md                    # Main documentation (this file)
├── ENHANCED_STATUS_SUMMARY.md   # Status bar enhancement documentation
├── zcam_control_reference.md    # Z CAM API quick reference
└── reterminal_slate_addons.md   # Enhancement roadmap and future features
```

## 🔄 Workflow Integration

### Recording Session
1. **F1** launches the podcast slate interface
2. **MARK** sends chapter markers during recording
3. **REC** starts Z CAM recording and timer
4. **PREVIEW** monitors camera feed in real-time
5. **F3** quickly closes preview when needed
6. Timer tracks recording duration with 15-minute auto-markers

### Post-Production
- MIDI markers exported to DAW timeline
- Z CAM recordings automatically timestamped
- Manual markers distinguish talking points from auto-chapters

## 🛠️ API Endpoints

### Z CAM Control
```bash
# Recording Control
GET http://10.98.33.1/ctrl/rec?action=start
GET http://10.98.33.1/ctrl/rec?action=stop

# Status Monitoring  
GET http://10.98.33.1/ctrl/info                    # Camera info
GET http://10.98.33.1/ctrl/get?k=battery          # Battery level
GET http://10.98.33.1/ctrl/get?k=movfmt           # Video format
GET http://10.98.33.1/ctrl/temperature            # Camera temperature
GET http://10.98.33.1/ctrl/get?k=iso              # ISO setting
GET http://10.98.33.1/ctrl/get?k=wb               # White balance
GET http://10.98.33.1/ctrl/card?action=query_free # Storage space
```

> **📖 See Also:** [Z CAM API Control Reference](zcam_control_reference.md) for complete endpoint documentation.

### MIDI Integration
- **Purple markers**: Manual chapter marks (button press) with MIDI note 60
- **Blue markers**: Automatic interval marks (15-minute timer) with MIDI note 62  
- **Output format**: MIDI messages to RODECaster Pro for DAW timeline integration
- **Local feedback**: 50ms 800Hz sine tone on 3.5mm audio jack for user confirmation

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

# Test API manually (basic)
curl "http://10.98.33.1/ctrl/rec?action=start"

# Test enhanced status endpoints
curl "http://10.98.33.1/ctrl/get?k=battery"
curl "http://10.98.33.1/ctrl/temperature"
curl "http://10.98.33.1/ctrl/get?k=movfmt"

# Check Z CAM WiFi connection
iwconfig wlan0
```

**Status Bar Diagnostics:**
- Check if status shows "WiFi OFF" - indicates connection issues
- Temperature showing "N/A" - API endpoint may be unavailable
- Storage showing "N/A" - card query endpoint issue

> **📖 Reference:** [Z CAM API Control Reference](zcam_control_reference.md) for endpoint troubleshooting.

### Display Problems
```bash
# Launch with proper environment
DISPLAY=:0 XAUTHORITY=/home/jharris/.Xauthority python3 main.py

# Check if app is actually running latest code
ps aux | grep main.py

# Force restart application
sudo pkill -f main.py
DISPLAY=:0 XAUTHORITY=/home/jharris/.Xauthority python3 main.py
```

### Browser Preview Issues
```bash
# Check available browsers
which chromium-browser firefox netsurf-gtk

# Test browser manually
chromium-browser --kiosk http://10.98.33.1/
```

### Network Configuration Issues
```bash
# Check network interfaces
ip addr show

# Verify Z CAM WiFi connection
ping -c 3 10.98.33.1

# Test Z CAM API endpoints
curl -s "http://10.98.33.1/ctrl/get?k=battery" | python3 -m json.tool

# Check route to Z CAM network
ip route | grep 10.98.33
```

### Development Access
```bash
# SSH via ethernet while WiFi connected to Z CAM
ssh jharris@<reterminal-ethernet-ip>

# Check both connections simultaneously
ping -I eth0 <development-network-gateway>
ping -I wlan0 10.98.33.1
```

## 🚦 Status Indicators

### Button Colors
- **MARK**: Purple (idle) → Bright purple (active flash)
- **REC**: Gray (idle) → Red (recording) → Orange (error)
- **PREVIEW**: Teal (idle) → Dark teal (active)

### Status Bar
The enhanced status bar displays comprehensive real-time information:

**Format:** `IP:10.98.33.1 • 6KP23.98 • 48°C • WB:Incandescent • ISO:6400 • 458.3GB • MIDI ON • WiFi ON`

- **IP Address**: Z CAM camera network address
- **Video Format**: Current recording format (6KP23.98, 4KP24, etc.)
- **Temperature**: Camera thermal status in Celsius
- **White Balance**: Current WB setting (Incandescent, Daylight, etc.)
- **ISO**: Current ISO setting (100, 800, 6400, etc.)
- **Storage**: Available SSD space in GB
- **MIDI Status**: RODECaster Pro connection status (ON/OFF)
- **WiFi Status**: Z CAM connectivity status (ON/OFF)

*Updates automatically every 5 seconds with graceful fallbacks to "N/A" for unavailable data.*

> **📖 See Also:** [Enhanced Status Bar Documentation](ENHANCED_STATUS_SUMMARY.md) for complete implementation details.

## 📈 Enhancement Roadmap

The reTerminal Podcast Slate includes comprehensive enhancement documentation:

- **[Enhanced Status Bar](ENHANCED_STATUS_SUMMARY.md)** - Complete implementation details for the comprehensive status monitoring system
- **[Z CAM API Reference](zcam_control_reference.md)** - Quick reference for Z CAM HTTP endpoints and integration
- **[Future Enhancements](reterminal_slate_addons.md)** - Planned features and enhancement roadmap

### Planned Features
- RGB LED indicators for recording status
- Foot-switch integration for hands-free operation
- Automatic backup workflows to network storage
- Advanced MIDI features and custom marker types
- Multi-camera support and switching capabilities

> **📖 See Also:** [Complete Enhancement Roadmap](reterminal_slate_addons.md) for detailed feature planning.

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

## 🔗 Documentation Links

### Project Documentation
- **[Enhanced Status Bar Implementation](ENHANCED_STATUS_SUMMARY.md)** - Comprehensive status monitoring features and API integration
- **[Z CAM API Control Reference](zcam_control_reference.md)** - Quick reference for reTerminal integration with Z CAM cameras
- **[Enhancement Roadmap](reterminal_slate_addons.md)** - Future features and development planning

### External References
- **[Z CAM Complete Documentation](../ZCAM-Documentation/)** - Comprehensive API reference and HTTP endpoints
- **[Seeed reTerminal Hardware](https://wiki.seeedstudio.com/reTerminal/)** - Official hardware documentation
- **[MIDI Technical Standard](https://www.midi.org/)** - MIDI protocol specifications
- **[GitHub Repository](https://github.com/neighborlyjim/reTerminal_Video_Studio)** - Source code and issue tracking
