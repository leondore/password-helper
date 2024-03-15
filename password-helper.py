#! python3

import os, sys, pyperclip
from cryptography.fernet import Fernet
from database import Database


def get_key():
    try:
        key = os.getenv("ENCRYPTION_KEY")
        if key is None:
            raise NameError("ENCRYPTION_KEY not found in environment variables")
        return key

    except NameError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def add_password(service, password):
    key = get_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode("utf-8"))

    passwords = Database()
    passwords.add_password(service, encrypted_password)
    passwords.close()


def get_password(service):
    key = get_key()
    cipher_suite = Fernet(key)

    passwords = Database()
    encrypted_password = passwords.get_password(service)
    passwords.close()

    if encrypted_password is None:
        return None
    return cipher_suite.decrypt(encrypted_password[0]).decode("utf-8")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("You must add at least one argument.", file=sys.stderr)
        sys.exit(1)

    if len(args) >= 2:
        add_password(args[0], args[1])
        print(f"Password for service: {args[0]} has been encrypted and saved.")
        return

    password = get_password(args[0])
    if password is None:
        print(f"No password was found for service: {args[0]}.", file=sys.stderr)
        sys.exit(1)

    pyperclip.copy(password)
    print(f"Password for service: {args[0]} has been copied to your clipboard.")


main()
