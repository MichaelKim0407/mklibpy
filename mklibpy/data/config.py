from . import list
from . import obj

__author__ = 'Michael'


class LoadConfig(object):
    def __init__(self, filename, var_name=None, obj_type=obj.DataObject, list_type=list.DataList):
        self.filename = filename
        self.var_name = var_name or filename.split(".")[0]
        self.obj_type = obj_type
        self.list_type = list_type

    def load(self):
        return self.list_type.load_file(self.filename, self.obj_type)
