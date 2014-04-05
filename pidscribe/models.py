from time import time
import ConfigParser
import psutil


class Process(object):
    """
    Create a process record from a psutil object.
    """
    def __init__(self, process):
        self.pid = process.pid
        self.name = process.name()
        self.time = time()
        self.process = process

    @property
    def run_time(self):
        """
        Get the the time a process has been running.
        """
        run_time = self.time - self.process.create_time()
        return run_time

    @property
    def running(self):
        """
        Check to see if the process is still running.
        """
        try:
            psutil.Process(pid=self.pid)
            running = True
        except psutil.NoSuchProcess:
            running = False
        return running


class User(object):
    """
    Create a user record from a psutil's list_users
    """
    def __init__(self, user):
        self.name = user.name
        self.time = time()
        self.user = user

    @property
    def usage_time(self):
        """
        Check to see how long the user has been logged in for.
        """
        usage_time = self.time - self.user.started
        return usage_time


class Config(object):
    """
    Load a configuration ini file with list of processes and users to monitor.
    """
    def __init__(self, config_path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_path)

    @property
    def users(self):
        """
        Return a list of users from the configuration file.
        """
        users = self.config.get('users', 'user_list').split(',')
        return users

    @property
    def processes(self):
        """
        Return a list of processes from the configuration file.
        """
        processes = self.config.get('processes', 'process_list').split(',')
        return processes

    def get_configuration_item(self, section, item):
        """
        Return an item from the configuration file.
        """
        return self.config.get(section, item)
