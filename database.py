import sqlite3


class Database:
    def __init__(self, database):
        self.database = database
        self.connection = None
        self.cursor = None

        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
