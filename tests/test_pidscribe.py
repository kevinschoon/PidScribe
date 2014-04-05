import subprocess
import unittest
from getpass import getuser
from pidscribe.models import Config, Process, User
from pidscribe.controller import get_processes, get_users, lookup_process_name, lookup_users


class TestProcess(unittest.TestCase):
    def setUp(self):
        sleep = ["sleep", "60"]
        self.process = subprocess.Popen(sleep).pid

    def test_get_processes(self):
        processes = get_processes()
        self.assertIsInstance(processes, list)

        for process in processes:
            self.assertIsInstance(process.pid, int)
            self.assertIsInstance(process.running, bool)
            self.assertIsInstance(process.run_time, float)

        named_lookup = lookup_process_name('sleep', processes)
        self.assertGreaterEqual(named_lookup, 1)


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.user = getuser()

    def test_get_users(self):
        users = get_users()
        self.assertIsInstance(users, list)

    def test_lookup_user(self):
        users = get_users()
        user_lookup = lookup_users(self.user, users)
        self.assertGreaterEqual(user_lookup, 1)


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.configuration_path = '../tests/pidscribe.ini'

    def test_load_configuration(self):
        config = Config(self.configuration_path)
        item = config.get_configuration_item('processes', 'process_list')
        self.assertIsInstance(item, str)
        self.assertIsInstance(config.processes, list)
        self.assertIsInstance(config.users, list)

if __name__ == '__main__':
    unittest.main()
