# Z CAM E‑Series Cont## 2. HTTP / CGI `ctrl` Endpoints

### Recording Control
| Example | Function |
|--------### Quick‑Reference for Your reTerminal Slate

* **REC button** — HTTP `/ctrl/rec?action=start|stop` (updated endpoint)
* **Status monitoring** — `/ctrl/get?k=battery|iso|wb|resolution` every 5 seconds
* **Preview** — `rtsp://192.168.8.1/live` → GStreamer  
* **Markers** — USB‑MIDI notes 60 & 62 to RØDECaster  
* **Sync blip** — Pi headphone → camera mic (or LTC on XLR)

**Status Display Format:**
```
🎹 MIDI Connected • Camera: Live 🔋 100% • ISO 6400 • Tungsten
📹 6K • 🎬 Auto
```

Everything you need to automate a Z CAM from Python or a hardware button box—on one sheet.----|
| `/ctrl/rec?action=start` | **Start recording** (used by reTerminal slate) |
| `/ctrl/rec?action=stop` | **Stop recording** (used by reTerminal slate) |

### Status Monitoring (Individual Key Queries)
| Example | Function | reTerminal Usage |
|---------|----------|------------------|
| `/ctrl/get?k=battery` | Battery percentage | Status bar display |
| `/ctrl/get?k=iso` | Current ISO setting | Exposure monitoring |
| `/ctrl/get?k=wb` | White balance setting | Color temp display |
| `/ctrl/get?k=resolution` | Recording resolution | Format confirmation |
| `/ctrl/get?k=shutter` | Shutter speed/angle | Exposure monitoring |

### Legacy CGI `zcmd` Endpoints (Reference Only)
| Example | Function |
|---------|----------|
| `/cgi-bin/zcmd?cmd=record&value=start` | **Start recording** (`value=stop` cuts) |
| `/cgi-bin/zcmd?cmd=still&value=1` | Capture still‑frame |
| `/cgi-bin/zcmd?cmd=iso&value=800` | ISO 800 |
| `/cgi-bin/zcmd?cmd=shutter&value=1/48` | Shutter 1/48 |
| `/cgi-bin/zcmd?cmd=wb&value=5600` | White‑balance 5600 K |
| `/cgi-bin/zcmd?cmd=iris&value=f2.8` | Electronic iris (EF/LPL) |
| `/cgi-bin/zcmd?cmd=videoformat&value=C4K24` | Resolution / FPS preset |
| `/cgi-bin/zcmd?cmd=vfrfps&value=120` | High‑speed VFR 120 fps |
| `/cgi-bin/zcmd?cmd=lut&value=on|off` | Monitor LUT toggle |
| `/cgi-bin/zcmd?cmd=fan&value=auto|high|low` | Fan profile |
| `/cgi-bin/zcmd?cmd=timecode&value=settocurrent` | TOD jam |
| `/cgi-bin/zcmd?cmd=info` | **JSON status** (`rec_state`, `timecode`, battery, temp …) |
A field‑ready catalogue of every control input and software request route a **Z CAM E2‑S6** (and siblings) accepts.

---

## 1. Physical & Electrical Control Inputs

| Port / Interface | Electrical spec | What you can drive / receive |
|------------------|-----------------|------------------------------|
| **2.5 mm REMOTE jack** (Menu ▸ System ▸ Remote Port) | • **LANC** open‑collector 5 V<br>• **UART 3.3 V** 115 200 N81 | • *LANC*: REC toggle, STILL, exposure (Sony 0x18 0x33 …)<br>• *UART‑Controller*: ASCII `rec start`, `iso 800`, etc. |
| **USB‑C** | USB 3.2 Gen‑1 | Mode‑selectable: **Network/RNDIS**, **PC Remote (PTP)**, **UVC**, **External SSD**, **MSC** |
| **RJ‑45 Gig‑E** | 1000BASE‑T | Same HTTP/CGI + RTSP as Network USB‑mode |
| **Wi‑Fi 2.4 GHz AP / Client** | 802.11 n | Same CGI + RTSP; SSID `ZCAM_xxxx`, PW `12345678` |
| **10‑pin LEMO I/O** | 3.3 V GPIO + trigger | Multi‑cam sync, tally, genlock trigger |
| **XLR‑5 / 3.5 mm MIC** | Analog audio **or** LTC | Linear time‑code, tone, scratch audio |
| **IR Remote** | NEC IR | Body button equivalents |
| **Body buttons & Fn** | GPIO | Local slate, quick settings |

---

## 2. HTTP / CGI `zcmd` Endpoints

| Example | Function |
|---------|----------|
| `/cgi-bin/zcmd?cmd=record&value=start` | **Start recording** (`value=stop` cuts) |
| `/cgi-bin/zcmd?cmd=still&value=1` | Capture still‑frame |
| `/cgi-bin/zcmd?cmd=iso&value=800` | ISO 800 |
| `/cgi-bin/zcmd?cmd=shutter&value=1/48` | Shutter 1/48 |
| `/cgi-bin/zcmd?cmd=wb&value=5600` | White‑balance 5600 K |
| `/cgi-bin/zcmd?cmd=iris&value=f2.8` | Electronic iris (EF/LPL) |
| `/cgi-bin/zcmd?cmd=videoformat&value=C4K24` | Resolution / FPS preset |
| `/cgi-bin/zcmd?cmd=vfrfps&value=120` | High‑speed VFR 120 fps |
| `/cgi-bin/zcmd?cmd=lut&value=on|off` | Monitor LUT toggle |
| `/cgi-bin/zcmd?cmd=fan&value=auto|high|low` | Fan profile |
| `/cgi-bin/zcmd?cmd=timecode&value=settocurrent` | TOD jam |
| `/cgi-bin/zcmd?cmd=info` | **JSON status** (`rec_state`, `timecode`, battery, temp …) |

---

## 3. UART (REMOTE ▸ Controller) ASCII Commands

```
115200 baud  8 N 1  3.3 V logic
```

| String | Effect |
|--------|--------|
| `rec start\r\n` | Start recording |
| `rec stop\r\n`  | Stop recording |
| `iso 800\r\n`   | ISO 800 |
| `wb 5600\r\n`   | WB 5600 K |
| `info\r\n`      | Same JSON as HTTP `/info` |

---

## 4. Sony LANC (REMOTE ▸ LANC) Byte Frames

| Function | 8‑byte hex payload |
|----------|--------------------|
| REC toggle | `18 33 00 00 00 00 00 00` |
| Zoom T / W | `18 33 2F 00 00 00 00 00` / `18 33 30 00 …` |
| Focus Near / Far | `18 33 38 00 …` / `18 33 39 00 …` |

9600 baud, even parity, 2 stop, open‑collector low pulses.

---

## 5. USB Personalities & Their Controls

| USB Mode | Host sees | Controllable via |
|----------|-----------|------------------|
| **Network (RNDIS/ECM)** | Virtual NIC + IP `192.168.8.1` | Full CGI + RTSP (`/live`) |
| **PC Remote (PTP)** | Vendor PTP device | `InitiateCapture`, property blocks |
| **UVC** | 1080p30 webcam | Basic UVC exposure toggles |
| **External SSD** | Host controller | No control during record |
| **MSC / Charge** | Mass‑storage | File copy only |

---

### Quick‑Reference for Your reTerminal Slate

* **REC button** — HTTP `/record&value=start|stop`  
* **Preview** — `rtsp://192.168.8.1/live` → GStreamer  
* **Markers** — USB‑MIDI notes 60 & 62 to RØDECaster  
* **Sync blip** — Pi headphone → camera mic (or LTC on XLR)

Everything you need to automate a Z CAM from Python or a hardware button box—on one sheet.
