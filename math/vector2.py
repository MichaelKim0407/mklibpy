"""
math/vector2.py create by Michael for mklibpy package.
"""

import types

import math
import mklibpy.code.func as func_util

__author__ = 'Michael'


class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(tuple):
        return Vector2(*tuple)

    @staticmethod
    def from_item(item):
        if isinstance(item, Vector2):
            return item
        elif isinstance(item, tuple):
            return Vector2.from_tuple(item)
        else:
            raise TypeError(item)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __format__(self, fmt):
        return "({}, {})".format(
            self.x.__format__(fmt),
            self.y.__format__(fmt)
        )

    # Comparison

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    # Calculation

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def len(self):
        return math.sqrt(self * self)

    def angle(self):
        return math.atan2(self.y, self.x)

    def float(self):
        return Vector2(float(self.x), float(self.y))

    # Hash

    def __hash__(self):
        return self.x.__hash__() * 13 + self.y.__hash__() * 17


zero = Vector2(0, 0)
up = Vector2(0, -1)
down = Vector2(0, 1)
left = Vector2(-1, 0)
right = Vector2(1, 0)


def convert_param(*names):
    def decor(cls_or_func):
        if isinstance(cls_or_func, type):
            cls = cls_or_func
            for name in cls.__dict__:
                if name in {"__dict__", "__doc__", "__module__"}:
                    continue
                attr = getattr(cls, name)
                new_attr = convert_param(*names)(attr)
                if isinstance(attr, types.FunctionType):
                    new_attr = staticmethod(new_attr)
                setattr(cls, name, new_attr)
            return cls

        elif isinstance(cls_or_func, types.FunctionType) \
                or isinstance(cls_or_func, types.MethodType):
            func = cls_or_func
            required_args = func_util.get_args(func)
            default_values = func_util.get_default_values(
                required_args, func.__defaults__
            )

            def __convert(_param_map):
                for name in _param_map:
                    if name in names:
                        _param_map[name] = Vector2.from_item(_param_map[name])

            if isinstance(cls_or_func, types.MethodType):
                required_args.remove("self")

                def new_func(self, *args, **kwargs):
                    param_map = func_util.get_param_map(
                        required_args, default_values,
                        args, kwargs
                    )
                    __convert(param_map)
                    return func(self, **param_map)
            else:
                def new_func(*args, **kwargs):
                    param_map = func_util.get_param_map(
                        required_args, default_values,
                        args, kwargs
                    )
                    __convert(param_map)
                    return func(**param_map)

            return new_func

        else:
            return cls_or_func

    return decor


def convert_attr(*names):
    def decor(cls):
        __setattr = cls.__setattr__

        def new_setattr(self, key, value):
            if key in names:
                value = Vector2.from_item(value)
            __setattr(self, key, value)

        setattr(cls, "__setattr__", new_setattr)
        return cls

    return decor
