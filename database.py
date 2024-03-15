import sqlite3


class Database:
    DB_NAME = "/home/ldore/projects/password-helper/passwords.db"

    def __init__(self):
        self.connection = sqlite3.connect(Database.DB_NAME)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def add_password(self, service, password):
        self.cursor.execute(
            "INSERT INTO passwords (service, password) VALUES (?, ?)",
            (service, password),
        )
        self.connection.commit()

    def get_password(self, service):
        self.cursor.execute(
            "SELECT password FROM passwords WHERE service=?", (service,)
        )
        return self.cursor.fetchone()
