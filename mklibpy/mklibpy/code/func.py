from . import types as _types

__author__ = 'Michael'


class FuncArgs(object):
    def __init__(self, func):
        self.count = func.__code__.co_argcount
        self.args = list(func.__code__.co_varnames[:self.count])

        if _types.is_method(func):
            self.count -= 1
            self.args.pop(0)

        if func.__defaults__ is None:
            self.count_default = 0
        else:
            self.count_default = len(func.__defaults__)
        self.count_required = self.count - self.count_default

        self.defaults = {}
        if func.__defaults__ is not None:
            for i in range(self.count_default):
                self.defaults[self.args[self.count_required + i]] = func.__defaults__[i]

    def __iter__(self):
        return iter(self.args)

    def push_no_extend(self, *args, **kwargs):
        if len(args) > self.count:
            raise TypeError("Too many positional arguments.")

        param_map = {}
        for i in range(self.count):
            arg_name = self.args[i]
            if i < len(args):
                param_map[arg_name] = args[i]
            elif arg_name in kwargs:
                param_map[arg_name] = kwargs[arg_name]
            elif arg_name in self.defaults:
                param_map[arg_name] = self.defaults[arg_name]
            else:
                raise TypeError("Missing positional argument '{}'".format(arg_name))

        return param_map

    def push(self, *args, **kwargs):
        param_map = self.push_no_extend(*args, **kwargs)

        for arg_name in kwargs:
            param_map[arg_name] = kwargs[arg_name]

        for arg_name in self.defaults:
            if arg_name not in param_map:
                param_map[arg_name] = self.defaults[arg_name]

        return param_map
