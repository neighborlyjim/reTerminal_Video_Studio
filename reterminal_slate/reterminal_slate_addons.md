# Optional Add‑Ons for the reTerminal Slate Console

Below are practical enhancements you can layer onto the three‑button **MARK / REC / PREVIEW** landscape UI.  
They’re grouped by effort so you can cherry‑pick the wins that fit your timeline.

| Effort bucket | Feature | Why it helps | Quick implementation hook |
|---------------|---------|--------------|---------------------------|
| **Zero‑cost UI (≤30 min)** | **Status bar** – connection LED, Wi‑Fi RSSI, SSD GB, battery/temp | One glance = safe to roll a 2 h show | Poll `…/cgi-bin/zcmd?cmd=info` every 5 s; update a 1280 × 40 frame |
|  | **MARK counter** – “5 manual / 8 auto” | Know post workload at a glance | Increment `manual_ct`, `auto_ct`; show under the timer |
| **One‑afternoon polish** | **Soft‑button lock** (press‑and‑hold 2 s) | Prevent fat‑finger hits | Long‑press timer label → `.config(state='disabled')` |
|  | **On‑screen interval slider** | Adjust chapter length on the fly | Double‑tap timer label → show `Scale`; reset scheduler |
| **Quality‑of‑life hardware (≈1 h wiring)** | **RGB LED ring** on GPIO 18/17/15 | Pulses purple/blue; solid red while rec | `gpiozero.RGBLED` in mark & rec callbacks |
|  | **Foot‑switch input** | Hands stay on faders; stomp to MARK | TRS tip→GPIO 26; `Button(26)` calls `purple_mark()` |
| **Content pipeline helpers** | **Slate note text‑box** | Embed “redo cold open” cue in log | `Entry` widget → write to `markers.log` with timestamp |
|  | **One‑tap card backup** | Auto `rsync` SSD + Rode SD to USB SSD | Spawn `rsync -a ...`; toast when `wait()==0` |
| **Advanced / stretch** | **Pi‑generated LTC** | Drop Tentacle; Pi feeds sync clock | Start `ltcgen`; route L‑ch to camera; mute beeps |
|  | **Sidus Link preset call** | Lights fade when timer stops | `requests.post` to Sidus Bridge `/command` in REC callback |

> **Tip:** Most add‑ons are pure Python. Only the LED ring & foot‑switch need two GPIO wires.
