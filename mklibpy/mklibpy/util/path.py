import os as _os

__author__ = 'Michael'


class CD(object):
    """
    Context manager.
    Changes working directory into the specified path,
    and returns to the previous directory after exiting.
    """

    def __init__(self, path):
        self.cwd = _os.path.abspath(_os.getcwd())
        self.path = _os.path.abspath(path)

    def __enter__(self):
        _os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        _os.chdir(self.cwd)


def ensure_path(path):
    """
    Ensures the path exists and is a directory.

    See also: ensure_dir

    :param path: The desired path
    """
    path = _os.path.abspath(path)
    if not _os.path.exists(path):
        ensure_dir(path)
        _os.mkdir(path)
    else:
        if _os.path.isfile(path):
            raise ValueError("Cannot create folder: \'{}\' is a file!".format(path))


def ensure_dir(path):
    """
    Ensures the dir containing path exists and is a directory.

    See also: ensure path

    :param path: The desired path
    """
    path = _os.path.abspath(path)
    ensure_path(_os.path.dirname(path))


def recursive(filter=None, dir_filter=None):
    if filter is None:
        def filter(x):
            return True
    if dir_filter is None:
        def dir_filter(x):
            return True

    def __decor(func):
        def __new_func(path):
            if _os.path.isdir(path):
                if not dir_filter(path):
                    return
                for name in sorted(_os.listdir(path)):
                    __new_func(_os.path.join(path, name))
                return

            if not filter(path):
                return

            func(path)

        return __new_func

    return __decor
