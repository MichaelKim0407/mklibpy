import mklibpy.error as _error

__author__ = 'Michael'


class OptionArg(object):
    def __init__(self, letter, fullname, opt_name, opt_value, trail=0):
        self.letter = letter
        self.fullname = fullname
        self.opt_name = opt_name
        self.opt_value = opt_value
        self.trail = trail

    def __eq__(self, other):
        return (self.letter is not None and other == self.letter) \
               or other == self.fullname


class Option(object):
    def __init__(self, value, *trail):
        self.value = value
        self.trail = list(trail)

    def __repr__(self):
        if self.trail:
            return "{} {}".format(self.value, self.trail)
        else:
            return "{}".format(self.value)


class ParsedArgs(dict):
    def __init__(self, seq=None, **kwargs):
        dict.__init__(self, seq, **kwargs)
        self.names = []

    def __repr__(self):
        return """\
Options:
    {}
Arguments:
    {}""".format(dict.__repr__(self), self.names)


class OptionArgList(list):
    def __init__(self, iterable=()):
        list.__init__(self, iterable)
        self.default = {}

    def set_default(self, **options):
        for key in options:
            v = options[key]
            if isinstance(v, Option):
                self.default[key] = v
            elif isinstance(v, tuple):
                self.default[key] = Option(*v)
            else:
                self.default[key] = Option(v)

    def parse(self, *args):
        result = ParsedArgs(self.default)

        def set_flag(arg, args):
            if arg not in self:
                raise _error.InvalidExecutionArgumentError(arg)
            _arg = self[self.index(arg)]
            trail = args[0:_arg.trail]
            result[_arg.opt_name] = Option(_arg.opt_value, *trail)
            return args[_arg.trail:]

        while args and args[0].startswith("-"):
            if args[0].startswith("--"):
                args = set_flag(args[0][2:], args[1:])
            else:
                letters = args[0][1:]
                args = args[1:]
                for letter in letters:
                    args = set_flag(letter, args)
        result.names.extend(args)
        return result
