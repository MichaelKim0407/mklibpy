from . import column as _column
from . import obj as _obj

__author__ = 'Michael'


class DataList(list):
    def __init__(self, iterable):
        list.__init__(self, iterable)

    def __getslice__(self, sli):
        return DataList(list.__getslice__(self, sli))

    def __add__(self, other):
        return DataList(list.__add__(self, other))

    def where(self, condition):
        return DataList([item for item in self if condition(item)])

    def column(self, name, method=None):
        if method is None:
            method = lambda x: x[name]
        col = [method(item) for item in self]
        return _column.Column(name, col)

    @classmethod
    def load_file(cls, filename, obj_type=_obj.DataObject):
        attr_keys = []

        def __load_file():
            with open(filename) as f:
                for line in f:
                    line = line.rstrip("\n")
                    if not attr_keys:
                        attr_keys.extend(line.split(obj_type.Split))
                    else:
                        yield obj_type.load(attr_keys, line)

        data_list = cls(__load_file())
        data_list.columns = attr_keys
        return data_list

    def save_file(self, filename):
        with open(filename, "w") as f:
            title = ""
            for c in self.columns:
                title += c + "\t"
            f.write(title[:-1] + "\n")
            for item in self:
                f.write(item.save(self.columns) + "\n")
