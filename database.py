import sqlite3, os, sys


class Database:
    DB_LOCATION = os.getenv("DB_PASSWORDS")

    def __init__(self):
        try:
            if Database.DB_LOCATION is None:
                raise NameError("DB_PASSWORDS not found in environment variables")

            self.connection = sqlite3.connect(Database.DB_LOCATION)
            self.cursor = self.connection.cursor()

        except NameError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    def close(self):
        self.connection.close()

    def add_password(self, service, password):
        try:
            result = self.cursor.execute(
                "INSERT INTO passwords (service, password) VALUES (?, ?)",
                (service, password),
            )
            self.connection.commit()
            return result
        except sqlite3.IntegrityError:
            return None

    def get_password(self, service):
        self.cursor.execute(
            "SELECT password FROM passwords WHERE service=?", (service,)
        )
        return self.cursor.fetchone()

    def delete_password(self, service):
        result = self.cursor.execute(
            "DELETE FROM passwords WHERE service=?", (service,)
        )
        self.connection.commit()
        return result
