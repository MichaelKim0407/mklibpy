"""
error.py create by Michael for mklibpy package.

Errors used in this package.
"""

__author__ = 'Michael'


class ValueSetLengthError(Exception):
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values

    def __repr__(self):
        return "The length of values ({}) is not equal to the length of keys ({})".format(len(self.values),
                                                                                          len(self.keys))


class InvalidExecutionArgumentError(Exception):
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return "Invalid option: {}".format(self.arg)


class VectorLengthError(Exception):
    def __init__(self, vec1, vec2):
        self.vec1 = vec1
        self.vec2 = vec2

    def __repr__(self):
        return "The length of {!r} is not equal to the length of {!r}".format(self.vec1, self.vec2)
