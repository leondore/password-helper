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
    cursor = passwords.add_password(service, encrypted_password)
    rows = cursor.rowcount

    passwords.close()

    return rows


def get_password(service):
    key = get_key()
    cipher_suite = Fernet(key)

    passwords = Database()
    encrypted_password = passwords.get_password(service)
    passwords.close()

    if encrypted_password is None:
        return None
    return cipher_suite.decrypt(encrypted_password[0]).decode("utf-8")


def delete_password(service):
    passwords = Database()
    cursor = passwords.delete_password(service)
    rows = cursor.rowcount

    passwords.close()

    return rows


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("You must add at least one argument.", file=sys.stderr)
        sys.exit(1)

    if len(args) >= 2:
        if args[0] == "delete":
            rows = delete_password(args[1])
            if rows == 0:
                print(f"No password was found for service: {args[1]}.", file=sys.stderr)
                sys.exit(1)

            print(f"Password for service: {args[1]} has been deleted.")
            return

        rows = add_password(args[0], args[1])
        if rows == 0:
            print(
                f"Password for service: {args[0]} could not been added.",
                file=sys.stderr,
            )
            sys.exit(1)

        print(f"Password for service: {args[0]} has been encrypted and saved.")
        return

    password = get_password(args[0])
    if password is None:
        print(f"No password was found for service: {args[0]}.", file=sys.stderr)
        sys.exit(1)

    pyperclip.copy(password)
    print(f"Password for service: {args[0]} has been copied to your clipboard.")


main()
