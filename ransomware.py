# -*- Coding : utf-8 -*-

from cryptography.fernet import Fernet

def save_key():
    key = Fernet.generate_key()
    with open("secret_key", "wb") as file:
        file.write(key)


def get_key():
    with open("secret_key", "rb") as file:
        return file.read()


def encrypt(filename):
    key = get_key()
    with open(filename, "rb") as file:
        content = file.read()

    encrypted_content = Fernet.encrypt(Fernet(key), content)

    with open(f"{filename}", "wb") as file:
        file.write(encrypted_content)


def decrypt(filename):
    key = get_key()
    with open(filename, "rb") as file:
        encrypted_content = file.read()

    content = Fernet.decrypt(Fernet(key), encrypted_content)

    with open(filename, "wb") as file:
        file.write(content)

if __name__ == "__main__":
    filename = input("Enter file name ")
    command = input("Enter action <encrypt> or <decrypt> ")

    if command == "encrypt":
        try:
            encrypt(filename)
            print(f"[+] Successfully encrypted {filename}")
        except Exception as e:
            print(f"[-] Encryption failed : {e}")

    elif command == "decrypt":
        try:
            decrypt(filename)
            print(f"[+] Successfully decrypted {filename}")
        except Exception as e:
            print(f"[-] Decryption failed.")
    else:
        print("[!!] Incorrect action entered.")
