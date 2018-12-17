from . import AbstractBooleanFunc as _Abs

__author__ = 'Michael'


class Equal(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, val):
        return val == self.__val


class LessThan(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, val):
        return val < self.__val


class GreaterThan(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, val):
        return val > self.__val


NotEqual = _Abs.NOT_CLASS(Equal)
LessThanOrEqual = _Abs.OR_CLASSES(Equal, LessThan)
GreaterThanOrEqual = _Abs.OR_CLASSES(Equal, GreaterThan)
