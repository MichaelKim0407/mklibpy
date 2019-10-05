import mklibpy.code.types as types
from mklibpy.code.decor import *

__author__ = 'Michael'


def returns(type):
    def __decor(func):
        def __new_func(*args, **kwargs):
            return type(func(*args, **kwargs))

        return __new_func

    return __decor


returns_str = returns(str)


@returns_str
def f(x):
    return x


def test_base():
    assert f(0) == '0'


@as_is(class_decorator(
    name_lambda=filter_not_special,
    attr_lambda=types.is_unbound_method,
)(returns_str))
class C(object):
    def f(self, x):
        return x


def test_class():
    assert C().f(0) == '0'


returns_str_mul = multipurpose_decorator(name_lambda=filter_not_special)(returns_str)


@returns_str_mul
def f2(x):
    return x


@returns_str_mul
class C2(object):
    def f(self, x):
        return x


def test_mul():
    assert f2(1) == '1'
    assert C2().f(1) == '1'


@with_params(multipurpose_decorator(name_lambda=filter_not_special))
def returns_2(type):
    return returns(type)


@returns_2(int)
def f3(x):
    return x


@returns_2(int)
class C3(object):
    def f(self, x):
        return x


def test_params():
    assert f3('0') == 0
    assert C3().f('0') == 0
