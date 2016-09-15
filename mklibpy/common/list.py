import mklibpy.code as code
import mklibpy.error as error

__author__ = 'Michael'

# We should ignore all methods that does not modify the content of the list
METHOD_IGNORE = {
    "__contains__",
    "__dir__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__iter__",
    "__le__",
    "__len__",
    "__lt__",
    "__repr__",
    "__str__"
}


def __unique_list_call(cls, unique):
    def __wrapper(func):
        def __new_func(*args, **kwargs):
            result = func(*args, **kwargs)
            if args and isinstance(args[0], cls):
                unique(args[0])
            return result

        return __new_func

    return __wrapper


def __make_unique_list(unique):
    def __wrapper(cls):
        return code.decor.make_class_decor_params(
            code.clazz.filter_name(lambda name: name not in METHOD_IGNORE)
        )(__unique_list_call)(cls, unique)(cls)

    return __wrapper


def __check_unique(l):
    s = set()
    for item in l:
        if item in s:
            raise error.RedundantValueError(item)
        s.add(item)


@__make_unique_list(__check_unique)
class UniqueList(list):
    pass
