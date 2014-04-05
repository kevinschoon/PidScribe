from models import Process, User
import psutil


def get_processes():
    """
    Get a list of all running processes.
    """
    processes = list()
    for process in psutil.get_process_list():
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

