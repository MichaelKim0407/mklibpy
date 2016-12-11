import mklibpy.util as _util

from . import column
from . import config
from . import list
from . import obj

__author__ = 'Michael'


class Data(object):
    def __init__(self):
        self.names = []

    def __getitem__(self, item):
        getattr(self, item)

    def __setitem__(self, key, value):
        self.names.append(key)
        self.__setattr__(key, value)

    def __repr__(self):
        return repr(self.names)


def load_files(dir_name, ext="", *files, **file_map):
    file_config_list = []
    for fname in files:
        file_config_list.append(config.LoadConfig(fname + ext))
    for fname in file_map:
        file_config_list.append(config.LoadConfig(fname + ext, *file_map[fname]))
    result = Data()
    with _util.path.CD(dir_name):
        for file_config in file_config_list:
            result[file_config.var_name] = file_config.load()
    return result
