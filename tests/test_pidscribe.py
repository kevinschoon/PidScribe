import subprocess
import unittest
from getpass import getuser
from pidscribe.models import Config, LoadedProcess, User
from pidscribe.util import get_md5_hash, check_if_running
from pidscribe.controller import Controller


class TestProcess(unittest.TestCase):
    def setUp(self):
        sleep = ["sleep", "60"]
        self.process = subprocess.Popen(sleep).pid
        self.process_name = 'sleep'

    def test_get_processes(self):
        processes = Controller.get_processes()
        self.assertIsInstance(processes, list)

        for process in processes:
            self.assertIsInstance(process.pid, int)
            self.assertIsInstance(process.running, bool)
            self.assertIsInstance(process.run_time, float)
            if process.md5_hash:
                self.assertIsInstance(process.md5_hash, str)

    def test_named_process_lookup(self):
        processes = Controller.get_processes()
        named_lookup = Controller.lookup_process_name(self.process_name, processes)
        self.assertGreaterEqual(named_lookup, 1)

    def test_config_lookup(self):
        process_list = get_processes()
        config = Config('pidscribe.ini')
        for process in config.processes:
            l = lookup_process_name(process, process_list)
            self.assertIsInstance(l, list)


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
