from mklibpy.logical.collection import (
    In, Contains,
    NotIn, DoesNotContain,
)

__author__ = 'Michael'


def test_base_classes():
    in_ = In('123')
    assert in_('1')
    assert not in_('0')
    assert str(in_) == "in '123'"

    contains = Contains('1')
    assert contains('123')
    assert not contains('023')
    assert str(contains) == "contains '1'"


def test_combined_classes():
    not_in = NotIn('123')
    assert not_in('0')
    assert not not_in('1')
    assert str(not_in) == "not (in '123')"

    not_contains = DoesNotContain('1')
    assert not_contains('023')
    assert not not_contains('123')
    assert str(not_contains) == "not (contains '1')"
