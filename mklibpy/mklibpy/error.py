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


class VectorLengthError(Exception):
    def __init__(self, vec1, vec2):
        self.vec1 = vec1
        self.vec2 = vec2

    def __str__(self):
        return "The length of {!r} is not equal to the length of {!r}".format(self.vec1, self.vec2)


class DuplicateValueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Value {!r} already exists.".format(self.value)
