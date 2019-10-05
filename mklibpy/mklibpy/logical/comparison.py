from . import (
    AbstractBooleanFunc as _Abs,
)

__author__ = 'Michael'


class Equal(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, val):
        return val == self.__val

    def __str__(self):
        return f"equals {self.__val!r}"


class LessThan(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, val):
        return val < self.__val

    def __str__(self):
        return f"less than {self.__val!r}"


class GreaterThan(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, val):
        return val > self.__val

    def __str__(self):
        return f"greater than {self.__val!r}"


NotEqual = _Abs.NOT_CLASS(Equal)
LessThanOrEqual = _Abs.OR_CLASSES(Equal, LessThan)
GreaterThanOrEqual = _Abs.OR_CLASSES(Equal, GreaterThan)
