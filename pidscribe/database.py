import sqlite3

class Database(object):
    """
    Connect to a SQLite database and update it with usage data.
    """
    def __init__(self):
        self.conn = sqlite3.connect('/tmp/pidscribe.sql')

    def initialize(self):
        pass

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
