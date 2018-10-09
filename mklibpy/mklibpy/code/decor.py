from . import clazz as _clazz
from . import types as _types

__author__ = 'Michael'


def make_decor_paramless(decor):
    """
    Decorates a @decorator, making it parameter-less.
    The @decorator must be callable without parameters.

    :param decor: The @decorator
    :return: The new @decorator
    """

    def __new_decor(decorated):
        return decor()(decorated)

    return __new_decor


def make_decor_params(decor):
    """
    Decorates a parameter-less @decorator, making it a decorator with 0 parameters.

    :param decor: The @decorator
    :return: The new @decorator
    """

    def __new_decor():
        return decor

    return __new_decor


def make_class_decor_params(*filters):
    """
    Decorate a @decorator targeting a function,
    making it a @decorator that targets a class.

    All matching methods will be decorated by the
    original @decorator.

    :return: The new @decorator
    """

    def __decor(func_decor):
        def __new_decor(*args, **kwargs):
            def __class_decor(cls):
                for name in _clazz.get_all_members(
                        cls,
                        _clazz.filter_item(_types.is_class_method),
                        *filters):
                    func = getattr(cls, name)
                    new_func = func_decor(*args, **kwargs)(func)
                    setattr(cls, name, new_func)
                return cls

            return __class_decor

        return __new_decor

    return __decor


def make_class_decor_paramless(*filters):
    """
    Decorate a parameter-less @decorator targeting a function,
    making it a @decorator that targets a class.

    All matching methods will be decorated by the
    original @decorator.

    See also: make_class_decor_params

    :return: The new @decorator
    """

    def __decor(func_decor):
        return make_decor_paramless(
            make_class_decor_params(*filters)(
                make_decor_params(func_decor)
            )
        )

    return __decor


def make_multipurpose_decor_params(*filters):
    def __decor(func_decor):
        def __new_decor(*args, **kwargs):
            def __inner_decor(cls_or_func):
                if _types.is_class(cls_or_func):
                    return make_class_decor_params(*filters)(func_decor)(*args, **kwargs)(cls_or_func)
                elif (_types.is_function | _types.is_class_method)(cls_or_func):
                    return func_decor(*args, **kwargs)(cls_or_func)
                else:
                    return cls_or_func

            return __inner_decor

        return __new_decor

    return __decor


def make_multipurpose_decor_paramless(*filters):
    def __decor(func_decor):
        return make_decor_paramless(
            make_multipurpose_decor_params(*filters)(
                make_decor_params(func_decor)
            )
        )

    return __decor
