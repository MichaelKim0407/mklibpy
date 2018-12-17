from mklibpy.logical.comparison import (
    Equal, LessThan, GreaterThan,
    NotEqual, LessThanOrEqual, GreaterThanOrEqual,
)

__author__ = 'Michael'


def test_base_classes():
    equal = Equal(1)
    assert equal(1)
    assert not equal(0)
    assert str(equal) == 'equals 1'

    less_than = LessThan(3)
    assert less_than(2)
    assert not less_than(3)
    assert str(less_than) == 'less than 3'

    greater_than = GreaterThan(3)
    assert greater_than(4)
    assert not greater_than(3)
    assert str(greater_than) == 'greater than 3'


def test_combined_classes():
    not_equal = NotEqual(1)
    assert not_equal(0)
    assert not not_equal(1)
    assert str(not_equal) == 'not (equals 1)'

    le = LessThanOrEqual(3)
    assert le(3)
    assert not le(4)
    assert str(le) == '(equals 3) or (less than 3)'

    ge = GreaterThanOrEqual(3)
    assert ge(3)
    assert not ge(2)
    assert str(ge) == '(equals 3) or (greater than 3)'
