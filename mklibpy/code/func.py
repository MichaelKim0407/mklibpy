__author__ = 'Michael'


def get_args(func):
    return list(func.__code__.co_varnames[:func.__code__.co_argcount])


def get_default_values(args, defaults):
    default_values = {}
    if defaults:
        j = len(args) - len(defaults)
        for i in range(len(defaults)):
            default_values[args[j]] = defaults[i]
            j += 1
    return default_values


def get_param_map(required_args, default_values, args, kwargs):
    if len(args) > len(required_args):
        raise SyntaxError("More unnamed arguments than required.")
    param_map = {}
    for i in range(len(required_args)):
        attr_name = required_args[i]
        if i < len(args):
            param_map[attr_name] = args[i]
        elif attr_name in kwargs:
            param_map[attr_name] = kwargs[attr_name]
        elif attr_name in default_values:
            param_map[attr_name] = default_values[attr_name]
        else:
            raise SyntaxError("Required argument \"{}\" not provided.".format(attr_name))
    for attr_name in kwargs:
        param_map[attr_name] = kwargs[attr_name]
    for attr_name in default_values:
        if attr_name not in param_map:
            param_map[attr_name] = default_values[attr_name]
    return param_map
