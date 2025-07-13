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
        _send(60, 800)   # NOTE 60, 800 Hz beep

def blue_mark():
    if out:
        _send(62, 800)   # NOTE 62, 800 Hz beep

def _send(note, freq):
    out.send(mido.Message('note_on', note=note, velocity=127))
    # Play 50ms sine tone at 800Hz on 3.5mm jack
    subprocess.Popen(
        ['play','-nq','-t','alsa','synth','0.05','sine','800'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
