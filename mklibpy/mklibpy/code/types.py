from __future__ import absolute_import

import types as _types

__author__ = 'Michael'


class __C1:
    def f(self):
        pass

    @staticmethod
    def fs():
        pass

    @classmethod
    def fc(cls):
        pass


class __C2(object):
    pass


LegacyClassType = type(__C1)
StandardClassType = type(__C2)

FunctionType = _types.FunctionType
BuiltinFunctionType = _types.BuiltinFunctionType

BoundMethodType = _types.MethodType
BuiltinMethodType = _types.BuiltinMethodType
WrapperMethodType = type([].__add__)

UnboundMethodType = type(__C1.f)
MethodDescriptorType = type(list.append)
WrapperDescriptorType = type(list.__add__)

StaticMethodType = type(__C1.fs)
ClassMethodType = type(__C1.fc)


class TypeOf(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return "{} {!r}".format(self.__class__.__name__, self.obj)

    def __eq__(self, other):
        return type(self.obj) == other

    def __ge__(self, other):
        return isinstance(self.obj, other)

    def __gt__(self, other):
        return self >= other and not (self == other)


class TypeCheck(object):
    def __init__(self, type=None, func=None):
        if type is None:
            if func is None:
                raise ValueError('type and func cannot be both None')
            self.func = func
        else:
            self.func = self.get_func(type)
            self.__str = "{}({})".format(self.__class__.__name__, type.__name__)

    def __str__(self):
        return self.__str

    @staticmethod
    def get_func(type):
        raise NotImplementedError

    @classmethod
    def and_(cls, *types):
        result = None
        for type in types:
            item = cls(type)
            if result is None:
                result = item
            else:
                result &= item
        return result

    @classmethod
    def or_(cls, *types):
        result = None
        for type in types:
            item = cls(type)
            if result is None:
                result = item
            else:
                result |= item
        return result

    def __call__(self, obj):
        return self.func(obj)

    def __and__(self, other):
        def __func(obj):
            return self(obj) and other(obj)

        t = TypeCheck(func=__func)
        t.__str = "({}) and ({})".format(self, other)
        return t

    def __or__(self, other):
        def __func(obj):
            return self(obj) or other(obj)

        t = TypeCheck(func=__func)
        t.__str = "({}) or ({})".format(self, other)
        return t

    def __sub__(self, other):
        def __func(obj):
            return self(obj) and not other(obj)

        t = TypeCheck(func=__func)
        t.__str = "({}) not ({})".format(self, other)
        return t


class IsExactType(TypeCheck):
    @staticmethod
    def get_func(type):
        def __func(obj):
            return TypeOf(obj) == type

        return __func


class IsInstance(TypeCheck):
    @staticmethod
    def get_func(type):
        def __func(obj):
            return TypeOf(obj) >= type

        return __func


is_class = IsInstance.or_(
    LegacyClassType,
    StandardClassType,
)
is_function = IsInstance.or_(
    FunctionType,
    BuiltinFunctionType,
)
is_bound_method = IsInstance.or_(
    BoundMethodType,
    BuiltinFunctionType,
    WrapperMethodType,
)
is_unbound_method = IsInstance.or_(
    UnboundMethodType,
    MethodDescriptorType,
    WrapperDescriptorType,
)
is_staticmethod = IsInstance(StaticMethodType)
is_classmethod = IsInstance(ClassMethodType)
is_class_method = is_unbound_method | is_staticmethod | is_classmethod
is_method = is_bound_method | is_class_method
