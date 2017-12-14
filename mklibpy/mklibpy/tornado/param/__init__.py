import re as _re

import tornado.web as _web

from . import types

__author__ = 'Michael Kim'

SPECIAL_TYPES = {"@body": types.BodyType}


class Param(object):
    def __init__(self, name, type=str, required=True):
        self.__name = name
        self.__type = type
        self.__required = required

    def get(self, handler):
        if self.__type is list:
            return {self.__name: handler.get_arguments(self.__name)}
        if self.__type is types.BodyType:
            return {self.__name: handler.request.body}

        try:
            val = handler.get_argument(self.__name)
        except _web.MissingArgumentError:
            if self.__required:
                raise
            else:
                return {}

        try:
            val = self.__type(val)
        except:
            pass
        else:
            return {self.__name: val}

        raise ParamTypeCastError(self, val)

    def __repr__(self):
        return "{} parameter <{}> \"{}\"".format(
            "Required" if self.__required else "Optional",
            self.__type.__name__,
            self.__name
        )


class ParamTypeCastError(Exception):
    def __init__(self, param, val):
        self.__param = param
        self.__val = val

    def __str__(self):
        return "Cannot cast parameter {!r}: value is {}".format(self.__param, self.__val)


class Params(list):
    docstring_paramtype_regex = _re.compile(":type ([^:]*): (.*)")

    def __init__(self, func=None):
        list.__init__(self)
        if func is not None:
            self(func)

    def __call__(self, func):
        argcount = func.__code__.co_argcount
        func_args = func.__code__.co_varnames[:argcount]
        defaults = len(func.__defaults__) if func.__defaults__ is not None else 0
        types = {}
        if func.__doc__:
            types = {tu[0].strip(): tu[1].strip()
                     for tu
                     in Params.docstring_paramtype_regex.findall(func.__doc__)}

        for i in range(argcount):
            name = func_args[i]
            if name in types:
                t = types[name]
                if t in SPECIAL_TYPES:
                    t = SPECIAL_TYPES[t]
                else:
                    t = eval(t)
            else:
                t = str
            self.add_param(
                name,
                t,
                i + defaults < argcount
            )

    def add_param(self, param, type=str, required=True):
        self.append(Param(param, type, required))

    def parse(self, handler):
        params = {}
        for p in self:
            params.update(p.get(handler))
        return params
