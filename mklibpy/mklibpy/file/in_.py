import mklibpy.common.collection as _collection
import mklibpy.util as _util

__author__ = 'Michael'


class MultiReader(object):
    def __init__(self, *names):
        self.__names = _collection.UniqueList(names)  # in __init__, make sure no file is opened twice

        self.__keys = _collection.UniqueList()  # in __enter__, make sure there are no duplicate keys
        self.__files = {}

        self.__fileiters = {}
        self.__current_lines = _collection.SequenceDict()
        self.nextline_flags = {}

    def __enter__(self):
        for name in self.__names:
            key = self.get_key(name)
            self.__keys.append(key)
            f = open(name)
            self.__files[key] = f
            self.__fileiters[key] = iter(f)
            self.__current_lines[key] = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key in self.__files:
            self.__files[key].close()

    def get_key(self, name):
        return name.rsplit(".", 1)[0]

    def __iter__(self):
        return self

    def __next(self):
        for key in self.__keys:
            # if False is explicitly specified in self.nextline_flags
            if key in self.nextline_flags and not self.nextline_flags[key]:
                continue

            fileiter = self.__fileiters[key]
            try:
                line = next(fileiter)
                line = line.rstrip()
            except StopIteration:
                line = None
            self.__current_lines[key] = line

        # if all files has eof
        for key in self.__keys:
            if self.__current_lines[key] is not None:
                break
        else:
            raise StopIteration

        # clear flags
        self.nextline_flags = {}
        return self.__current_lines.copy()

    if _util.osinfo.PYTHON2:
        def next(self):
            return self.__next()
    else:
        def __next__(self):
            return self.__next()
