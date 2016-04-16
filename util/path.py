"""
util/path.py create by Michael for mklibpy package.

Utility for file system paths.
"""

import os

__author__ = 'Michael'


class CD(object):
    def __init__(self, path):
        self.cwd = os.path.abspath(os.getcwd())
        self.path = os.path.abspath(path)

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.cwd)


def ensure_path(path):
    path = os.path.abspath(path)
    if not os.path.exists(os.path.dirname(path)):
        ensure_path(os.path.dirname(path))
    if not os.path.exists(path):
        os.mkdir(path)
