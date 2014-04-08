from models import LoadedProcess, LoadedUser, ProcessError, Config
from database import Database
from time import sleep
import psutil


class Controller(object):
    def __init__(self):
        self.processes = psutil.process_iter
        self.users = psutil.users

    def lookup_process_name(self, process_name):
        """
        From a list of processes, find a process by it's name.
        """
        processes = list()
        for process in self.processes():
            if process_name == process.name():
                processes.append(LoadedProcess(process))
        return processes

    def lookup_user_name(self, user_name):
        """
        From a list of users, find a user by their name.
        """
        users = list()
        for user in self.users():
            if user_name == user.name:
                users.append(LoadedUser(user))
        return users

    def start(self):
        """
        Run a simple daemon for now.
        """
        monitor_all_processes = True
        db = Database()
        conf = Config('../tests/pidscribe.ini')
        while True:
            if monitor_all_processes:
                for process in self.processes():
                    try:
                        loaded_process = LoadedProcess(process)
                        db.record_process(loaded_process)
                    except ProcessError:
                        pass
            else:
                for process in self.processes():
                    if [p for p in conf.processes if p == process.name()]:
                        try:
                            loaded_process = LoadedProcess(process)
                            db.record_process(loaded_process)
                        except ProcessError:
                            pass
            print('Sleeping...')
            sleep(15)

if __name__ == '__main__':
    c = Controller()
    db = Database()
    c.start()

