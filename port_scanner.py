import socket
from IPy import IP

class PortScanner():

    def __init__(self, target, port):
        self.target = target
        self.port = port

    def check_ip(self):
        try:
            return IP(self.target)
        except ValueError:
            try:
                return socket.gethostbyname(self.target)
            except Exception as e:
                print(f"[E] An error occurred : {e}")
                exit(0)

    def scan(self):
        print(f"\n[*] Scanning target -> {self.target}")
        host = self.check_ip()

        for port in range(1, int(self.port) + 1):
            self.scan_host(port)

    def scan_host(self, port=22):
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((self.target, port))
            try:
                bannner = ": " + sock.recv(1024).decode()
            except :
                banner = ""
            print(f"[+] Port {port} is open {banner}")
        except :
            pass

if __name__ == "__main__":

    target = input("Enter the target/s (comma separated) you want to scan: ")
    port = input("Enter the ports range (500 -> 500 first ports) : ")

    portscanner = PortScanner(target, port)

    if "," in portscanner.target:
        for target in portscanner.target.strip(" ").split(","):
            portscanner.target = target
            portscanner.scan()
    else:
        portscanner.scan()