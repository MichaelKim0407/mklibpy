from collections import defaultdict

from mklibpy.code.types import *

__author__ = 'Michael'


class C:
    def f(self):
        pass

    @staticmethod
    def fs():
        pass

    @classmethod
    def fc(cls):
        pass


class C2(object):
    def f(self):
        pass

    @staticmethod
    def fs():
        pass

    @classmethod
    def fc(cls):
        pass


def test_eq():
    assert TypeOf(1) == int
    assert TypeOf('a') == str
    t = TypeOf(defaultdict())
    assert t != dict
    assert t == defaultdict


def test_ge():
    t = TypeOf(defaultdict())
    assert t >= dict
    assert t >= defaultdict
    assert t > dict
    assert not (t > defaultdict)


def test_is_exact():
    assert IsExactType(int)(1)
    assert IsExactType(str)('0')
    assert not IsExactType(dict)(defaultdict())


def test_isinstance():
    assert IsInstance(int)(1)
    assert IsInstance(str)('0')
    assert IsInstance(dict)(defaultdict())


def test_function():
    assert is_function(test_eq)
    assert is_function(lambda: None)


def test_class():
    assert is_class(int)
    assert is_class(C)
    assert is_class(C2)


def test_method():
    assert is_unbound_method(C.f)
    assert is_bound_method(C().f)
    assert is_staticmethod(C.fs)
    assert is_staticmethod(C().fs)
    assert is_classmethod(C.fc)
    assert is_classmethod(C().fc)

    assert is_unbound_method(C2.f)
    assert is_bound_method(C2().f)
    assert is_staticmethod(C2.fs)
    assert is_staticmethod(C2().fs)
    assert is_classmethod(C2.fc)
    assert is_classmethod(C2().fc)
