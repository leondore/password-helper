import sqlite3


class Database:
    DB_NAME = "/home/ldore/projects/password-helper/passwords.db"

    def __init__(self):
        self.connection = sqlite3.connect(Database.DB_NAME)
        self.cursor = self.connection.cursor()

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
