import threading

_local = threading.local()


def set_current_user(user):
    _local.user = user


def get_current_user():
    return getattr(_local, 'user', None)


def set_current_ip(ip):
    _local.ip = ip


def get_current_ip():
    return getattr(_local, 'ip', None)


def clear():
    if hasattr(_local, 'user'):
        del _local.user
    if hasattr(_local, 'ip'):
        del _local.ip
