import sqlite3


class DatabaseError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class Database(object):
    """
    Connect to a SQLite database and update it with usage data.
    """
    def __init__(self):
        self.conn = sqlite3.connect('/tmp/pidscribe.sql')
        self.initialize()

    def record_process(self, scribed_process=None, scribed_user=None):
        if not scribed_process or scribed_user:
            raise DatabaseError('You need to pass either a scribed_process or scribed_user to update the database.')

        if scribed_process:
            print('Tracking process: {}'.format(scribed_process.md5_hash))
            assert scribed_process.name
            assert scribed_process.run_time
            assert scribed_process.md5_hash

            if self.retrieve_process(scribed_process.md5_hash):
                self.update_process(scribed_process.name, scribed_process.pid, scribed_process.run_time,
                                    scribed_process.md5_hash)
            else:
                self.insert_process(process_name=scribed_process.name, process_id=scribed_process.pid,
                                process_run_time=scribed_process.run_time, process_hash=scribed_process.md5_hash)

    def initialize(self):
        c = self.conn.cursor()
        try:
            c.execute('''
            CREATE TABLE processes(id INTEGER PRIMARY KEY, process_name STRING, process_id INT, process_run_time FLOAT,
            process_hash STRING)
            ''')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
        try:
            c.execute('''
            CREATE TABLE users(id INTEGER PRIMARY KEY, process_name STRING, user_id, INT, group_id, INT,
            usage_time, INT)
            ''')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def retrieve_process(self, md5_hash):
        c = self.conn.cursor()
        sql_response = list()
        c.execute('''
        SELECT process_name, process_id, process_run_time, process_hash FROM processes WHERE process_hash = ?
        ''', (md5_hash,))
        for row in c:
            sql_response.append(row)
        return sql_response

    def insert_process(self, process_name, process_id, process_run_time, process_hash):
        c = self.conn.cursor()
        c.execute('''
        INSERT INTO processes(process_name, process_id, process_run_time, process_hash)
        VALUES(?,?,?,?)
        ''', (process_name, process_id, process_run_time, process_hash)
        )
        self.conn.commit()

    def update_process(self, process_name, process_id, process_run_time, process_hash):
        c = self.conn.cursor()
        c.execute('''
        UPDATE processes SET process_name = ?, process_id = ?, process_run_time = ? WHERE process_hash = ?
        ''', (process_name, process_id, process_run_time, process_hash))
        self.conn.commit()

    def delete(self):
        pass
