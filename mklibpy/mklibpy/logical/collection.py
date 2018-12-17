from . import AbstractBooleanFunc as _Abs

__author__ = 'Michael'


class In(_Abs):
    def __init__(self, collection):
        self.__col = collection

    def __call__(self, val):
        return val in self.__col


class Contains(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, collection):
        return self.__val in collection


NotIn = _Abs.NOT_CLASS(In)
DoesNotContain = _Abs.NOT_CLASS(Contains)
