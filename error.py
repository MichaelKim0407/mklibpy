"""
error.py create by Michael for mklibpy package.

Errors used in this package.
"""

__author__ = 'Michael'


class ValueSetLengthError(Exception):
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values

    def __str__(self):
        return "The length of values ({}) is not equal to the length of keys ({})".format(len(self.values),
                                                                                          len(self.keys))


class InvalidExecutionArgumentError(Exception):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "Invalid option: {}".format(self.arg)
