
import requests


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


domain = input("[*] Enter target domain (url without http) : ")
print("[*] Running ...\n")
count = 0

with open("common_url.txt", "r") as file:
    for line in file.readlines():
        line = line.strip()

        subdomain_url = f"{line}.{domain}"
        dir_url = f"{domain}/{line}"
        subdomain = request(subdomain_url)
        directory = request(dir_url)

        if subdomain:
            print(f"[+] Subdomain found at : {subdomain_url}")
            count += 1

        if directory:
            print(f"[+] Directory found at : {dir_url}")
            count += 1

    print(f"\n[*] End of task. Total results found : {count}")
