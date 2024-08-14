import socket
import os
import platform
import subprocess
import threading
import struct

from termcolor import colored
import ipaddress
from scapy.all import sr1, IP, TCP


PROGRESS = 0
ACTIVE_HOSTS = []

def ip_to_bin(ip):
    """Convert an IP address to its binary form."""
    return struct.unpack('!I', socket.inet_aton(ip))[0]


def bin_to_ip(binary):
    """Convert a binary form IP address to its standard dotted notation."""
    return socket.inet_ntoa(struct.pack('!I', binary))


def calculate_network_address(ip, subnet_mask):
    """Calculate the network address from the given IP and subnet mask."""
    ip_bin = ip_to_bin(ip)
    mask_bin = ip_to_bin(subnet_mask)
    network_bin = ip_bin & mask_bin
    return bin_to_ip(network_bin)


def get_subnet_mask(cidr):
    """Get the subnet mask from the CIDR notation."""
    return str(ipaddress.IPv4Network(f"0.0.0.0/{cidr}").netmask)


def get_all_ips_in_range(network_address, cidr):
    """Generate all IP addresses within the subnet."""
    network = ipaddress.IPv4Network(f"{network_address}/{cidr}", strict=False)
    return [str(ip) for ip in network.hosts()]


def ping_host(ip):
    """Ping a host to check if it is up."""
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    command = ["ping", param, ip]

    # Redirect stdout and stderr to /dev/null to suppress output
    with open(os.devnull, 'w') as devnull:
        response = subprocess.call(command, stdout=devnull, stderr=devnull)

    return response == 0


def scan_ports(ip):
    """Scan common ports on the host to check if they are open."""
    open_ports = []
    common_ports = [22, 80, 443, 21, 23, 25, 110, 445]  # You can expand this list

    for port in range(1, 500):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    return open_ports


def detect_service(port):
    """Attempt to detect the service running on a given port."""
    service_name = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        21: "FTP",
        23: "Telnet",
        25: "SMTP",
        110: "POP3",
        445: "SMB"
    }
    return service_name.get(port, "Unknown Service")


def detect_os(ip):
    """Attempt to detect the operating system of a host using TCP/IP fingerprinting."""
    try:
        pkt = IP(dst=ip) / TCP(dport=80, flags="S")
        response = sr1(pkt, timeout=1, verbose=0)
        if response:
            ttl = response.ttl
            if ttl <= 64:
                return "Linux/Unix"
            elif ttl > 64 and ttl <= 128:
                return "Windows"
            else:
                return "Unknown OS"
        return "No Response"
    except Exception as e:
        return f"Error: {str(e)}"


def scan_host(ip):
    global PROGRESS
    """Scan a single host for active status, open ports, and OS detection."""
    if ping_host(ip):

        # Detect OS
        os_info = detect_os(ip)

        # Scan ports and detect services
        open_ports = scan_ports(ip)
        services = []
        for port in open_ports:
            services.append({"port": port, "name": detect_service(port)})

        ACTIVE_HOSTS.append({
            "ip" : ip,
            "os" : os_info,
            "services" : services
        })

    PROGRESS += 1
    end()


def end():
    global PROGRESS
    print(PROGRESS)


def main():
    ip_range = "192.168.241.15/24"

    ip, cidr = ip_range.split("/")

    subnet_mask = get_subnet_mask(cidr)
    net_addr = calculate_network_address(ip, subnet_mask)

    all_ips = get_all_ips_in_range(net_addr, cidr)

    threads = []

    # Discover and scan hosts concurrently
    for ip in all_ips:
        scan_host(ip)
        thread = threading.Thread(target=scan_host, args=(ip,))
        threads.append(thread)
        # thread.start()

    # Wait for all threads to finishE
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()


