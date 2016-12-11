import mklibpy.code as _code
import mklibpy.error as _error
import mklibpy.util as _util

__author__ = 'Michael'


class StandardList(list):
    # --- conversions ---

    CONVERSION_ACCEPT_LIST = True
    CONVERSION_ACCEPT_TUPLE = False

    @classmethod
    def from_list(cls, obj):
        return cls(*obj)

    @classmethod
    def from_tuple(cls, obj):
        return cls(*obj)

    @classmethod
    def from_item(cls, obj, accept_list=None, accept_tuple=None):
        if accept_list is None:
            accept_list = cls.CONVERSION_ACCEPT_LIST
        if accept_tuple is None:
            accept_tuple = cls.CONVERSION_ACCEPT_TUPLE

        if isinstance(obj, cls):
            return cls
        elif accept_list and isinstance(obj, list):
            return cls.from_list(obj)
        elif accept_tuple and isinstance(obj, tuple):
            return cls.from_tuple(obj)
        else:
            raise TypeError(obj)

    # --- Code simplification ---

    @classmethod
    @_code.decor.make_multipurpose_decor_params(
        _code.clazz.filter_item(_code.types.is_func_or_method))
    def convert_params(cls, *names, **kwargs):
        """
        Decorate a function or a class,
        so that all parameters whose name is in *names
        will be converted.

        :param names:
            A list of names.

        :param kwargs:
            Arguments for class.from_item except the first one.

        :return: @decorator
        """

        def __wrapper(func):
            required_args = _code.func.get_args(func)
            default_values = _code.func.get_default_values(
                required_args, func.__defaults__
            )

            def __convert(_param_map):
                for name in _param_map:
                    if name in names:
                        _param_map[name] = cls.from_item(_param_map[name], **kwargs)

            if _code.types.is_method(func):
                # required_args.remove("self")
                required_args.pop(0)

                def new_func(self, *args, **kwargs):
                    param_map = _code.func.get_param_map(
                        required_args, default_values,
                        args, kwargs
                    )
                    __convert(param_map)
                    return func(self, **param_map)
            else:
                def new_func(*args, **kwargs):
                    param_map = _code.func.get_param_map(
                        required_args, default_values,
                        args, kwargs
                    )
                    __convert(param_map)
                    return func(**param_map)

            return new_func

        return __wrapper

    @classmethod
    def convert_attr(cls, *names, **kwargs):
        """
        Decorate a class,
        so that all members whose name is in *names
        will be converted.

        :param names:
            A list of names.

        :param kwargs:
            Arguments for class.from_item except the first one.

        :return: @decorator
        """

        def __wrapper(decorated_cls):
            __setattr = decorated_cls.__setattr__

            def new_setattr(self, key, value):
                if key in names:
                    value = cls.from_item(value, **kwargs)
                __setattr(self, key, value)

            setattr(decorated_cls, "__setattr__", new_setattr)
            return decorated_cls

        return __wrapper

    # --- list methods ---

    if _util.osinfo.PYTHON2:  # list.clear does not exists in Python 2
        def clear(self):
            self[:] = []
            # or self *= 0

    def copy(self, cls=None):
        if cls is None:
            cls = self.__class__
        return cls(self)

    if _util.osinfo.PYTHON2:  # list.sort in Python 2 & 3 are different
        def sort(self, key=None, reverse=False):
            list.sort(self, None, key, reverse)
    else:
        def sort(self, key=None, reverse=False):
            list.sort(self, key=key, reverse=reverse)

    def split(self, size, cls=None, container=None):
        if not isinstance(size, int):
            raise TypeError(size)
        if size <= 0:
            raise ValueError(size)

        if cls is None:
            cls = self.__class__

        if container is None:
            container = StandardList

        def __gen():
            __size = 0
            __this = cls()

            for item in self:
                __size += 1
                __this.append(item)
                if __size == size:
                    yield __this
                    __size = 0
                    __this = cls()

            if __size > 0:
                yield __this

        return container(__gen())


# We should ignore all methods that does not modify the content of the list,
# or does not create a conflict.
LIST_METHOD_IGNORE = {
    "__add__",
    "__contains__",
    "__delitem__",
    "__dir__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getitem__",
    "__gt__",
    "__iter__",
    "__le__",
    "__len__",
    "__lt__",
    "__mul__",
    "__repr__",
    "__reversed__",
    "__sizeof__",
    "__str__",
    "clear",
    "copy",
    "count",
    "index",
    "pop",
    "remove",
    "reverse",
    "sort"
}


def __post_list_call(cls, func):
    def __wrapper(method):
        def __new_method(*args, **kwargs):
            if args and isinstance(args[0], cls):
                __backup = list(args[0])
                result = method(*args, **kwargs)
                try:
                    func(args[0])
                except Exception:
                    args[0][:] = __backup
                    raise
                return result
            else:
                return method(*args, **kwargs)

        return __new_method

    return __wrapper


def __make_list(func):
    def __wrapper(cls):
        return _code.decor.make_class_decor_params(
            _code.clazz.filter_name(lambda name: name not in LIST_METHOD_IGNORE)
        )(__post_list_call)(cls, func)(cls)

    return __wrapper


def __check_unique(l):
    s = set()
    for item in l:
        if item in s:
            raise _error.DuplicateValueError(item)
        s.add(item)


@__make_list(__check_unique)
class UniqueList(StandardList):
    """
    A list in which all values must be unique.
    Any operation that inserts a duplicate value will raise an mklibpy.error.DuplicateValueError.
    """
    pass


class SequenceDict(object):
    """
    A dictionary in which keys are sequenced.
    """

    def __init__(self, *args, **kwargs):
        self.__keys = UniqueList()
        self.__dict = {}

        for key in args:
            self.__keys.append(key)
            if key in kwargs:
                self.__dict[key] = kwargs[key]
            else:
                self.__dict[key] = None
        for key in kwargs:
            if key in args:
                continue
            self.__keys.append(key)
            self.__dict[key] = kwargs[key]

    def __repr__(self):
        return _util.collection.format_dict(self, sort=False)

    # --- Container methods ---
    # See: https://docs.python.org/3/reference/datamodel.html#emulating-container-types

    def __len__(self):
        return self.__keys.__len__()

    def __getitem__(self, item):
        return self.__dict.__getitem__(item)

    def __setitem__(self, key, value):
        if key not in self.__keys:
            self.__keys.append(key)
        self.__dict.__setitem__(key, value)

    def __delitem__(self, key):
        self.__keys.remove(key)
        self.__dict.__delitem__(key)

    def __iter__(self):
        return self.__keys.__iter__()

    def __reversed__(self):
        return self.__keys.__reversed__()

    def __contains__(self, item):
        return self.__keys.__contains__(item)

    # --- SequenceDict operations ---

    def clear(self):
        self.__keys.clear()
        self.__dict.clear()

    def copy(self):
        return SequenceDict(*self.__keys, **self.__dict)

    def index(self, value, start=None, stop=None):
        if start is None:
            return self.__keys.index(value)
        elif stop is None:
            return self.__keys.index(value, start)
        else:
            return self.__keys.index(value, start, stop)

    def insert(self, index, key, value):
        self.__keys.insert(index, key)
        self[key] = value

    def keys(self):
        return list(self.__keys)

    def pop(self, key):
        self.__keys.remove(key)
        return self.__dict.pop(key)

    def pop_at(self, index):
        key = self.__keys.pop(index)
        val = self.__dict.pop(key)
        return key, val

    def reverse(self):
        self.__keys.reverse()

    def sort(self, key=None, reverse=False):
        self.__keys.sort(key=key, reverse=reverse)

    def sort_by_value(self, key=None, reverse=False):
        if key is not None:
            key = lambda x: key(self[x])
        self.__keys.sort(key=key, reverse=reverse)

    def values(self):
        def __gen():
            for key in self:
                yield self[key]

        return list(__gen())


def __check_type(l):
    for item in l:
        if not isinstance(item, l.TYPE):
            raise TypeError("{!r} is not of type {}".format(item, l.TYPE))


@__make_list(__check_type)
class __TypedList(StandardList):
    TYPE = object


__typed_list_classes = {}


def typed_list_cls(type):
    if type in __typed_list_classes:
        return __typed_list_classes[type]
    else:
        class __new_cls(__TypedList):
            TYPE = type

        __typed_list_classes[type] = __new_cls
        return __new_cls


class BinaryArray(typed_list_cls(bool)):
    def to_int(self):
        result = 0
        for item in self:
            result *= 2
            if item:
                result += 1
        return result

    @classmethod
    def from_int(cls, value, size):
        result = cls()
        while size > 0:
            if value % 2 == 1:
                result.insert(0, True)
                value -= 1
            else:
                result.insert(0, False)
            value /= 2
            size -= 1
        return result

    @classmethod
    def iter_all(cls, size):
        # We can also use range(2 ** size) and from_int
        if not isinstance(size, int):
            raise TypeError(size)
        if size < 0:
            raise ValueError(size)

        if size == 0:
            yield []
            return

        for this in [False, True]:
            for append in BinaryArray.iter_all(size - 1):
                yield cls([this] + append)


class AnyCollection(object):
    DEFAULT_LIST_TYPE = StandardList

    # --- initialization ---

    def __init__(self, objects=[], li_cls=None, cls=None):
        self.__li_cls = self.DEFAULT_LIST_TYPE if li_cls is None else li_cls
        self.__li = self.__make_list(objects, li_cls)

        if cls is None:
            cls = self.__class__
        self.__cls = cls

    # --- content list ---

    @classmethod
    def _make_list(cls, objects):
        if cls == AnyCollection:
            return StandardList(objects)
        try:
            return cls.DEFAULT_LIST_TYPE(objects)
        except:
            return cls.__base__._make_list(objects)

    def __make_list(self, objects, li_cls):
        try:
            return li_cls(objects)
        except:
            try:
                return self.__li_cls(objects)
            except:
                return self._make_list(objects)

    def __iter__(self):
        return self.__li.__iter__()

    def items(self, li_cls=None):
        return self.__make_list(self.__li, li_cls)

    def add(self, *objects):
        self.__li.extend(objects)

    # --- to str ---

    def __repr__(self):
        return "*" + repr(self.__li)

    # --- transformations ---

    @classmethod
    def _make_collection(cls, *args, **kwargs):
        if cls == AnyCollection:
            return AnyCollection(*args, **kwargs)
        try:
            return cls(*args, **kwargs)
        except:
            return cls.__base__._make_collection(*args, **kwargs)

    def __getattribute(self, name):
        result = [getattr(obj, name) for obj in self]
        return self.__cls._make_collection(result, self.__li_cls, self.__cls)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return self.__getattribute(name)

    def __call__(self, *args, **kwargs):
        result = [obj(*args, **kwargs) for obj in self]
        return self.__cls._make_collection(result, self.__li_cls, self.__cls)

    def call(self, call, *args, **kwargs):
        result = [call(obj, *args, **kwargs) for obj in self]
        return self.__cls._make_collection(result, self.__li_cls, self.__cls)

    # --- nonzero: True or False ---

    if _util.osinfo.PYTHON2:
        def __nonzero__(self):
            for obj in self:
                if obj:
                    return True
            return False
    else:
        def __bool__(self):
            for obj in self:
                if obj:
                    return True
            return False

    def __len__(self):
        count = 0
        for obj in self:
            if obj:
                count += 1
        return count

    # --- standard methods ---

    @classmethod
    def add_method(cls, name):
        def __method(self, *args, **kwargs):
            return self.__getattribute(name)(*args, **kwargs)

        setattr(cls, name, __method)

    @classmethod
    def add_methods(cls, *names):
        for name in names:
            cls.add_method(name)


# See: https://docs.python.org/3/reference/datamodel.html
__ANY_COLLECTION_ADD_METHODS = {
    "__lt__", "__le__", "__eq__", "__ne__", "__gt__", "__ge__",
    "__contains__",
    "__neg__", "__pos__", "__abs__", "__invert__",
    "__complex__", "__int__", "__float__", "__round__"
}

__MATH_OPERATORS = {
    "add", "sub", "mul", "matmul", "truediv", "floordiv", "mod", "divmod", "pow", "lshift", "rshift", "and", "xor", "or"
}

for __oper in __MATH_OPERATORS:
    __ANY_COLLECTION_ADD_METHODS.add("__{}__".format(__oper))
    __ANY_COLLECTION_ADD_METHODS.add("__r{}__".format(__oper))

AnyCollection.add_methods(*__ANY_COLLECTION_ADD_METHODS)
