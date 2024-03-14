#! python3

import os, sys
from cryptography.fernet import Fernet


def get_key():
    try:
        key = os.getenv("ENCRYPTION_KEY")
        if key is None:
            raise NameError("ENCRYPTION_KEY not found in environment variables")
        return key

    except NameError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    key = get_key()

    print(key)


main()
