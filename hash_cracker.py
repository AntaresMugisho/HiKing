# -*- Coding : utf-8 -*-

"""
    Brute force hash.
"""

import termcolor
import hashlib, sys

hash_type = input("[*] Enter hash type : ")
hash_to_decrypt = input("[*] Enter hash value to brute force : ")
print("[*] Processing ...\n")

with open("common.txt", "r") as file:
    for password in file.readlines():
        if hash_type.lower() == "md5":
            hash_object = hashlib.md5(password.strip().encode())
            hashed_psw = hash_object.hexdigest()

            if hashed_psw == hash_to_decrypt:
                print(termcolor.colored(f"[+] Found MD5 Password: {password.strip()}", "green"))
                sys.exit(0)

        if hash_type.lower() == "sha1":
            hash_object = hashlib.sha1(password.strip().encode())
            hashed_psw = hash_object.hexdigest()

            if hashed_psw == hash_to_decrypt:
                print(termcolor.colored(f"[+] Found SHA1 Password: {password.strip()}", "green"))
                sys.exit(0)

    print(termcolor.colored("[-] Sorry, No matching password found !", "red"))