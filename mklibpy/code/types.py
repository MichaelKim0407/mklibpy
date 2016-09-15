from __future__ import absolute_import

import types

__author__ = 'Michael'


# FIXME Things work really differently in Python 2 and Python 3.


def is_class(obj):
    return isinstance(obj, type)


def is_func(obj):
    return isinstance(obj, types.FunctionType)


def is_method(obj):
    return isinstance(obj, types.MethodType)


def is_func_or_method(obj):
    return is_func(obj) or is_method(obj)
