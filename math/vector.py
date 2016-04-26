"""
math/vector.py create by Michael for mklibpy package.
"""

import types

import mklibpy.code.func as func_util
import mklibpy.error as error
import mklibpy.util as util

__author__ = 'Michael'


class Vector(list):
    Length = None
    AttrNames = dict()

    def __init__(self, *values, **kwargs):
        if self.__class__.Length is None:
            list.__init__(self, values)
        else:
            list.__init__(self)
            zero = kwargs["zero"] if "zero" in kwargs else None
            for i in range(self.__class__.Length):
                if i < len(values):
                    list.append(self, values[i])
                else:
                    list.append(self, zero)

    def __getattribute__(self, item):
        if item != "__class__" and item in self.__class__.AttrNames:
            return self[self.__class__.AttrNames[item]]
        else:
            return object.__getattribute__(self, item)

    @classmethod
    def from_tuple(cls, item):
        return cls(*item)

    @classmethod
    def from_item(cls, item):
        if isinstance(item, cls):
            return item
        elif isinstance(item, tuple):
            return cls.from_tuple(item)
        else:
            raise TypeError(item)

    # Formatting

    def __repr__(self):
        return self.__class__.__name__ + " " + util.list.to_str(self, start="(", end=")")

    def __str__(self):
        return util.list.to_str(self, split=" ", start="", end="")

    def __format__(self, spec):
        return self.format(spec).__str__()

    # Conversion

    def convert(self, func):
        return self.__class__(*[func(x) for x in self])

    def int(self):
        return self.convert(int)

    def float(self):
        return self.convert(float)

    def format(self, spec):
        return self.convert(lambda x: format(x, spec))

    # Comparison

    def check_length(self, other):
        if not isinstance(other, Vector):
            raise TypeError(other)
        if list.__len__(self) != list.__len__(other):
            raise error.VectorLengthError(self, other)

    def __eq__(self, other):
        self.check_length(other)
        for i in self.range():
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    # Dimensions

    def range(self):
        return range(len(self))

    def select(self, id_list, vec_type=None):
        if vec_type is None:
            vec_type = Vector
        return vec_type(*[self[i] for i in id_list])

    def reduce(self, n, vec_type=None):
        return self.select(range(n), vec_type)

    def slice(self, i, j, vec_type=None):
        return self.select(range(i, j), vec_type)

    def extend(self, n, vec_type=None, val=None):
        return vec_type(*(list(self) + [val] * (n - len(self))))

    # Calculation

    @classmethod
    def add_operator(cls, method_name):
        def method(self):
            return cls(*[getattr(x, method_name)() for x in self])

        setattr(cls, method_name, method)

    @classmethod
    def add_operator_bi(cls, method_name):
        def method(self, other):
            self.check_length(other)
            return cls(*[getattr(self[i], method_name)(other[i]) for i in self.range()])

        setattr(cls, method_name, method)

    def __neg__(self):
        return self.__class__(*[-x for x in self])

    def __add__(self, other):
        self.check_length(other)
        return self.__class__(*[self[i] + other[i] for i in self.range()])

    def __sub__(self, other):
        self.check_length(other)
        return self.__class__(*[self[i] - other[i] for i in self.range()])

    def __mul__(self, other):
        if isinstance(other, Vector):
            self.check_length(other)
            result = 0
            for i in self.range():
                result += self[i] * other[i]
            return result
        else:
            return self.__class__(*[x * other for x in self])

    def __rmul__(self, other):
        return self * other

    def squared(self):
        return self * self

    def length(self):
        return (self * self) ** 0.5

    # Constant

    @classmethod
    def identical(cls, value, length=None):
        if length is None:
            if cls.Length is None:
                raise ValueError(length)
            length = cls.Length
        return cls(*[value] * length)

    @classmethod
    def zero_int(cls, length=None):
        return cls.identical(0, length)

    @classmethod
    def zero_float(cls, length=None):
        return cls.identical(0.0, length)

    @classmethod
    def unit(cls, zero, value, i, length=None):
        if length is None:
            if cls.Length is None:
                raise ValueError(length)
            length = cls.Length
        return cls(*([zero] * i + [value] + [zero] * (length - i - 1)))

    @classmethod
    def unit_int(cls, i, length=None):
        return cls.unit(0, 1, i, length)

    @classmethod
    def unit_float(cls, i, length=None):
        return cls.unit(0.0, 1.0, i, length)

    # Code simplification

    @classmethod
    def convert_param(vec_type, *names):
        def decor(cls_or_func):
            if isinstance(cls_or_func, type):
                cls = cls_or_func
                for name in cls.__dict__:
                    if name in {"__dict__", "__doc__", "__module__"}:
                        continue
                    attr = getattr(cls, name)
                    new_attr = vec_type.convert_param(*names)(attr)
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
                            _param_map[name] = vec_type.from_item(_param_map[name])

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

    @classmethod
    def convert_attr(vec_type, *names):
        def decor(cls):
            __setattr = cls.__setattr__

            def new_setattr(self, key, value):
                if key in names:
                    value = vec_type.from_item(value)
                __setattr(self, key, value)

            setattr(cls, "__setattr__", new_setattr)
            return cls

        return decor
