__author__ = 'Michael'


class AbstractBooleanFunc(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return ''

    def __repr__(self):
        return f"<Boolean> {self}"

    @staticmethod
    def NOT(func):
        return BooleanFunc(
            lambda *args, **kwargs:
            not func(*args, **kwargs),
            str=f"not ({func})",
        )

    def __neg__(self):
        return self.NOT(self)

    @staticmethod
    def NOT_CLASS(cls):
        return lambda *args, **kwargs: -cls(*args, **kwargs)

    @staticmethod
    def AND(f1, f2):
        return BooleanFunc(
            lambda *args, **kwargs:
            f1(*args, **kwargs) and f2(*args, **kwargs),
            str=f"({f1}) and ({f2})",
        )

    def __and__(self, other):
        return self.AND(self, other)

    @staticmethod
    def AND_CLASSES(cls1, cls2):
        return lambda *args, **kwargs: cls1(*args, **kwargs) & cls2(*args, **kwargs)

    @staticmethod
    def OR(f1, f2):
        return BooleanFunc(
            lambda *args, **kwargs:
            f1(*args, **kwargs) or f2(*args, **kwargs),
            str=f"({f1}) or ({f2})",
        )

    def __or__(self, other):
        return self.OR(self, other)

    @staticmethod
    def OR_CLASSES(cls1, cls2):
        return lambda *args, **kwargs: cls1(*args, **kwargs) | cls2(*args, **kwargs)

    @classmethod
    def init(cls, x=None, *args, **kwargs):
        if not isinstance(x, AbstractBooleanFunc):
            pass
        elif args or kwargs:
            pass
        else:
            return x
        return cls(x, *args, **kwargs)


class BooleanFunc(AbstractBooleanFunc):
    def __init__(self, func, str=None):
        self.__func = func
        self.__str = str

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    def __str__(self):
        if self.__str is not None:
            return self.__str
        else:
            return repr(self.__func)
