from . import collection

__author__ = 'Michael'


class String(str):
    def split(self, sep=None, maxsplit=-1):
        return StringCollection(str.split(self, sep, maxsplit))

    def rsplit(self, sep=None, maxsplit=-1):
        return StringCollection(str.rsplit(self, sep, maxsplit))

    def splitlines(self, keepends=None):
        return StringCollection(str.splitlines(self, keepends))

    def startswith(self, prefix, start=None, end=None):
        if isinstance(prefix, StringCollection):
            return prefix.other_startswith(self, start=None, end=None)
        else:
            return str.startswith(self, prefix, start, end)

    def endswith(self, suffix, start=None, end=None):
        if isinstance(suffix, StringCollection):
            return suffix.other_endswith(self, start=None, end=None)
        else:
            return str.endswith(self, suffix, start, end)

    def __contains__(self, item):
        if isinstance(item, StringCollection):
            return item.other_contains(self)
        else:
            return str.__contains__(self, item)


class StringCollection(collection.AnyCollection):
    DEFAULT_LIST_TYPE = collection.typed_list_cls(str)

    def other_startswith(self, other, start=None, end=None):
        return self.call(other.startswith, start=None, end=None)

    def other_endswith(self, other, start=None, end=None):
        return self.call(other.endswith, start=None, end=None)

    def other_contains(self, other):
        return self.call(other.__contains__)