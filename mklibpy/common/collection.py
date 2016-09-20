import mklibpy.code as code
import mklibpy.error as error
import mklibpy.util as util

__author__ = 'Michael'


class StandardList(list):
    if util.osinfo.PYTHON2:
        def clear(self):
            self[:] = []
            # or self *= 0

    def copy(self, cls=None):
        if cls is None:
            cls = self.__class__
        return cls(self)

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
        return code.decor.make_class_decor_params(
            code.clazz.filter_name(lambda name: name not in LIST_METHOD_IGNORE)
        )(__post_list_call)(cls, func)(cls)

    return __wrapper


def __check_unique(l):
    s = set()
    for item in l:
        if item in s:
            raise error.DuplicateValueError(item)
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
        return util.collection.format_dict(self, sort=False)

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

    if util.osinfo.PYTHON2:
        def sort(self, cmp=None, key=None, reverse=False):
            self.__keys.sort(cmp, key, reverse)

        def sort_by_value(self, cmp=None, key=None, reverse=False):
            if cmp is not None:
                cmp = lambda x, y: cmp(self[x], self[y])
            if key is not None:
                key = lambda x: key(self[x])
            self.__keys.sort(cmp, key, reverse)
    else:
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
            raise TypeError(item)


@__make_list(__check_type)
class TypedList(StandardList):
    TYPE = object


class BinaryArray(TypedList):
    TYPE = bool

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
