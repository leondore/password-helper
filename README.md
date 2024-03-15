# Password Helper

Save passwords encrypted in sqlite3 db, and decrypt and copy from command line. Built in Python.

## Description

Simple password helper that allows you to save passwords encrypted in a sqlite3 database, and decrypt and copy them to clipboard from the command line. Requires an encryption key to encrypt and decrypt the passwords. This needs to be set in the environment variable `ENCRYPTION_KEY`. Also requires a sqlite3 database file to be set in the environment variable `DB_PASSWORDS`.
