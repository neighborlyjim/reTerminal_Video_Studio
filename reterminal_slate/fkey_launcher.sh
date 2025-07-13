#!/bin/bash
# F-key listener and app launcher for reTerminal
# Requires: evtest (sudo apt-get install evtest)
export DISPLAY=:0
export XAUTHORITY=/home/jharris/.Xauthority
FKEY_DEVICE="/dev/input/event0"
APP_CMD="/home/jharris/reterminal_slate_venv/bin/python /home/jharris/reTerminal_Video_Studio/reterminal_slate/main.py"

sudo stdbuf -oL evtest "$FKEY_DEVICE" | while read -r line; do
    echo "DEBUG: $line" # Show every line for troubleshooting
    # F1 (KEY_A, code 30)
    if echo "$line" | grep -q "type 1 (EV_KEY), code 30 (KEY_A), value 1"; then
        echo "F1 (KEY_A) detected, launching app!"
        $APP_CMD &
        sleep 1
    fi
    # F2 (KEY_S, code 31)
    if echo "$line" | grep -q "type 1 (EV_KEY), code 31 (KEY_S), value 1"; then
        echo "F2 (KEY_S) detected!"
        # Add your F2 action here
        sleep 1
    fi
    # F3 (KEY_D, code 32)
    if echo "$line" | grep -q "type 1 (EV_KEY), code 32 (KEY_D), value 1"; then
        echo "F3 (KEY_D) detected!"
        # Add your F3 action here
        sleep 1
    fi
    # Green button (KEY_F, code 33)
    if echo "$line" | grep -q "type 1 (EV_KEY), code 33 (KEY_F), value 1"; then
        echo "Green button (KEY_F) detected!"
        # Add your green button action here
        sleep 1
    fi
done
