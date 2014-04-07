from models import Process, User
from database import Database
from time import sleep
import psutil


def get_processes():
    """
    Get a list of all running processes.
    """
    processes = list()
    for process in psutil.get_process_list():
        print('Loading process: {}').format(process)
        processes.append(Process(process))
    return processes


def get_users():
    """
    Get a list of all logged in users.
    """
    users = list()
    for user in psutil.get_users():
        users.append(User(user))
    return users


def lookup_process_name(process_name, process_list):
    """
    From a list of processes, find a process by it's name.
    """
    response = list()
    for process in process_list:
        if process.name == process_name and process.running:
            response.append(process)
    return response


def lookup_users(user_name, user_list):
    """
    From a list of users, find a user by their name.
    """
    response = list()
    for user in user_list:
        if user_name == user.name:
            response.append(user)
    return response

def run():
    """
    Run a simple daemon for now.
    """
    db = Database()
    while True:
        print('Loading processes..')
        processes = get_processes()
        for process in processes:
            #TODO: How do I watch THIS process?
            #TODO: How to handle processes that close?
            if process.name == 'python2.7':
                pass
            else:
                print('PROCESS:{}, PID:{}, PROCESS_RUN_TIME:{}, BIN_HASH:{}'.format(process.name, process.pid,
                                                                                    process.run_time, process.md5_hash))
        print('Sleeping....')
        sleep(15)

if __name__ == '__main__':
    run()
