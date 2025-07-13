import mido, subprocess

RC_PORT = 'RODECaster Pro MIDI 1'   # enumerate once on boot
out = None
midi_status = 'Not connected'
def check_midi():
    global out, midi_status
    try:
        out = mido.open_output(RC_PORT)
        midi_status = 'Connected'
    except (OSError, IOError):
        out = None
        midi_status = 'Not connected'
    return midi_status
check_midi()

def purple_mark():
    if out:
        _send(60, 1000)   # NOTE 60, 1 kHz beep for manual markers

def blue_mark():
    if out:
        _send(62, 800)   # NOTE 62, 800 Hz beep for auto markers

def _send(note, freq):
    out.send(mido.Message('note_on', note=note, velocity=127))
    # Play tone at specified frequency on 3.5mm jack
    subprocess.Popen(
        ['play','-nq','-t','alsa','synth','0.05','sine',str(freq)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
