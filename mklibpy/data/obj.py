import mklibpy.util as _util

__author__ = 'Michael'


class DataObject(object):
    KeyMap = {}
    Split = "\t"

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __getitem__(self, key):
        return getattr(self, key)

    def __setattr__(self, key, value):
        if key in self.__class__.KeyMap:
            key = self.__class__.KeyMap[key]
        object.__setattr__(self, key, value)
        if isinstance(value, str):
            try:
                object.__setattr__(self, key, float(value))
                object.__setattr__(self, key, int(value))
            except ValueError:
                if value == "":
                    object.__setattr__(self, key, None)

    def __repr__(self):
        return repr(self.__dict__)

    @classmethod
    def load(cls, columns, line):
        values = line.split(cls.Split)
        return cls(**_util.collection.to_dict(columns, values))

    def save(self, columns):
        result = ""
        for c in columns:
            val = self[c]
            if val is None:
                val = ""
            else:
                val = str(val)
            result += val + self.__class__.Split
        return result[:-1]
