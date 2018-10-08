import mklibpy.code.types as types
from mklibpy.code.attrs import AttributesOf

__author__ = 'Michael'


class C(object):
    def __init__(self):
        self.x = 0

    def f(self):
        pass


class C2(C):
    def f2(self):
        pass


def test_class():
    attrs = AttributesOf(C).attrs
    assert '__init__' in attrs
    assert 'f' in attrs
    assert attrs['f'] == C.f


def test_object():
    c = C()
    attrs = AttributesOf(c).attrs
    assert 'f' in attrs
    assert attrs['f'] == c.f
    assert 'x' in attrs
    assert attrs['x'] == c.x


def test_filter_1():
    attrs = AttributesOf(
        str,
        name_endswith='with',
    ).attrs
    assert set(attrs.keys()) == {'startswith', 'endswith'}


def test_filter_2():
    attrs = AttributesOf(
        C,
        attr_lambda=types.is_unbound_method,
    ).self_attrs
    assert set(attrs.keys()) == {'__init__', 'f'}


def test_inherit():
    a = AttributesOf(C2)
    assert 'f2' in a.attrs
    assert 'f2' in a.self_attrs
    assert 'f' in a.attrs
    assert 'f' not in a.self_attrs


def test_extend():
    c = C2()
    assert AttributesOf(c, name_startswith='f').attrs == \
           AttributesOf(c).filter(name_startswith='f').attrs
