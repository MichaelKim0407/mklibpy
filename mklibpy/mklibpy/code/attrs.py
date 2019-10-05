from cached_property import (
    cached_property,
)

__author__ = 'Michael'


class AttributesOf(object):
    def __init__(self, obj, **kwargs):
        self.obj = obj
        self.__filters = self.filters(**kwargs)

    @staticmethod
    def filters(
            name_in=None,
            name_startswith=None,
            name_endswith=None,
            name_exclude=None,
            name_lambda=None,
            attr_lambda=None,
            full_lambda=None,
    ):
        filters = []

        if name_in is not None:
            if isinstance(name_in, str):
                name_in = [name_in]
            filters.append(lambda name, attr: name in name_in)
        if name_startswith is not None:
            filters.append(lambda name, attr: name.startswith(name_startswith))
        if name_endswith is not None:
            filters.append(lambda name, attr: name.endswith(name_endswith))
        if name_exclude is not None:
            if isinstance(name_exclude, str):
                name_exclude = [name_exclude]
            filters.append(lambda name, attr: name not in name_exclude)
        if name_lambda is not None:
            filters.append(lambda name, attr: name_lambda(name))
        if attr_lambda is not None:
            filters.append(lambda name, attr: attr_lambda(attr))
        if full_lambda is not None:
            filters.append(full_lambda)

        return filters

    def filter(self, **kwargs):
        new = AttributesOf(self.obj, **kwargs)
        new.__filters += self.__filters
        return new

    def __match(self, name, attr):
        for filter in self.__filters:
            if not filter(name, attr):
                return False
        return True

    @cached_property
    def self_attrs(self):
        result = {}
        for name in self.obj.__dict__:
            attr = getattr(self.obj, name)
            if not self.__match(name, attr):
                continue
            result[name] = attr
        return result

    @cached_property
    def attrs(self):
        result = {}
        for name in dir(self.obj):
            attr = getattr(self.obj, name)
            if not self.__match(name, attr):
                continue
            result[name] = attr
        return result
