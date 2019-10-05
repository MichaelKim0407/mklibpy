from . import (
    attrs as _attrs,
    types as _types,
)

__author__ = 'Michael'


def as_is(x):
    """
    Circumvent the decorator syntax limit by wrapping the result in a function call.

    E.g.
        @decorator_list[0]
    will result in SyntaxError, however
        @as_is(decorator_list[0])
    is accepted.
    """
    return x


def class_decorator(**filters):
    """
    Decorate a @decorator targeting a function,
    making it a @decorator that targets a class.

    All matching methods will be decorated by the
    original @decorator.

    :return: The new @decorator
    """

    # TODO: staticmethod and classmethod

    def __decor(func_decor):
        def __class_decor(cls):
            for name, func in _attrs.AttributesOf(
                    cls,
                    attr_lambda=_types.is_class_method,
            ).filter(**filters).attrs.items():
                new_func = func_decor(func)
                setattr(cls, name, new_func)
            return cls

        return __class_decor

    return __decor


def multipurpose_decorator(**filters):
    def __decor(func_decor):
        def __inner_decor(cls_or_func):
            if _types.is_class(cls_or_func):
                return class_decorator(**filters)(func_decor)(cls_or_func)
            elif (_types.is_function | _types.is_class_method)(cls_or_func):
                return func_decor(cls_or_func)
            else:
                return cls_or_func

        return __inner_decor

    return __decor


def with_params(decor_decor):
    """
    Decorate a @decorator targeting a decorator,
    making it accept and return param-decorators.
    """

    def __new_decor_decor(decor_with_params):
        def __new_decor_with_params(*args, **kwargs):
            return decor_decor(decor_with_params(*args, **kwargs))

        return __new_decor_with_params

    return __new_decor_decor


def filter_not_special(name):
    return not name.startswith('__')
