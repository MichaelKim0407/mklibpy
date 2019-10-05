from . import (
    AbstractBooleanFunc as _Abs,
)

__author__ = 'Michael'


class In(_Abs):
    def __init__(self, collection):
        self.__col = collection

    def __call__(self, val):
        return val in self.__col

    def __str__(self):
        return f"in {self.__col!r}"


class Contains(_Abs):
    def __init__(self, val):
        self.__val = val

    def __call__(self, collection):
        return self.__val in collection

    def __str__(self):
        return f"contains {self.__val!r}"


NotIn = _Abs.NOT_CLASS(In)
DoesNotContain = _Abs.NOT_CLASS(Contains)
