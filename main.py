import nmap
import ipaddress
import struct
import socket

from termcolor import colored


# HELPER FUNCTIONS
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


def discover_hosts(ip_range):
    """Utilise Nmap pour découvrir les hôtes actifs sur le réseau."""
    scanner = nmap.PortScanner()
    scanner.scan(hosts=ip_range, arguments='-sn')

    active_hosts = []
    for host in scanner.all_hosts():
        if scanner[host].state() == "up":
            active_hosts.append(host)

    return active_hosts


def scan_os_and_services(ip):
    """Utilise Nmap pour découvrir le système d'exploitation et les services sur une IP donnée."""
    scanner = nmap.PortScanner()
    scan_result = scanner.scan(ip, arguments='-O -sV')

    try:
        os_info = scan_result['scan'][ip]['osmatch'][0]['name'] if 'osmatch' in scan_result['scan'][ip] else 'Unknown OS'
    except IndexError:
        os_info = "Unknown OS"
    services = []

    if 'tcp' in scan_result['scan'][ip]:
        for port in scan_result['scan'][ip]['tcp']:
            service = scan_result['scan'][ip]['tcp'][port]['name']
            product = scan_result['scan'][ip]['tcp'][port]['product']
            version = scan_result['scan'][ip]['tcp'][port]['version']
            state = scan_result['scan'][ip]['tcp'][port]['state']
            services.append({'port': port, 'service': service, 'state': state, "product": product, "version": version})

    return os_info, services


def main():
    ip_range = "192.168.241.48/24"

    ip, cidr = ip_range.split("/")

    subnet_mask = get_subnet_mask(cidr)
    net_addr = calculate_network_address(ip, subnet_mask)

    all_ips = get_all_ips_in_range(net_addr, cidr)

    print(colored("[+] Network address ->", "green"), colored(f"{net_addr}", "blue", attrs=["bold"]))
    print(colored("[+] Subnet mask ->", "green"), colored(f"{subnet_mask}", "blue", attrs=["bold"]))

    print(colored(f"\n[!] Scanning a total of {len(all_ips)} hosts ...", "blue"))

    active_hosts = discover_hosts(ip_range)
    print(colored(f"[+] Found", "blue"),
          colored(f"{len(active_hosts)}", "blue", attrs=["bold"]),
          colored(f"active hosts.", "blue")
    )
    for host in active_hosts:
        print(colored(f"    [+] » {host}", "green"))

    for ip in active_hosts:
        print(colored(f"\n[!] Scanning host {ip}", "blue"))
        os_info, services = scan_os_and_services(ip)

        print(colored(f"    [+] » OS: {os_info}", "green"))
        print(colored(f"    [+] » Services:", "green"))

        if services:
            for service in services:
                print(colored(f"           - Port {service['port']}: {service['service']} ({service['state']}) {service['product']} {' ' if not service['version'] else 'v' + service['version']}", "green"))
        else:
            print(colored("          [x] No running service found here !", "red"))


if __name__ == "__main__":
    main()
