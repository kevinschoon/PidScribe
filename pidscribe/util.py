import psutil
from hashlib import md5


def check_if_running(pid):
    """
    Check to see if the process is still running.
    """
    return psutil.pid_exists(pid)


def get_md5_hash(file_path):
    """
    Return the hash of a file at the given file path.
    """
    hash = md5()
    f = open(file_path)
    while True:
        data = f.read(128)
        if not data:
            break
        hash.update(data)
    md5_hash = str(hash.hexdigest())
    return md5_hash
