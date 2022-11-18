import socket
from IPy import IP

def check_ip(target):
    try:
        return IP(target)
    except ValueError:
        return socket.gethostbyname(target)

def scan(target):
    print(f"\n[...] Scanning target -> {target}")
    host = check_ip(target)

    for port in range(20, 81):
        scan_host(host, port)

def scan_host(host, port=80):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((host, port))
        print(f"[+] Port {port} is open")
    except:
        pass

if __name__ == "__main__":
    targets = input("Enter the target/s (comma separated) you want to scan: ")

    if "," in targets:
        for target in targets.strip(" ").split(","):
            scan(target)
    else:
        scan(targets)