import json as _json

__author__ = 'Michael'


def format_config(config, make_copy=False, **kwargs):
    if make_copy:
        import copy as _copy
        config = _copy.deepcopy(config)

    def is_str(_val):
        return isinstance(_val, str) or isinstance(_val, unicode)

    def format_str(format_string, recursion_depth=2):
        # see: string.Formatter.vformat
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in format_string._formatter_parser():
            if literal_text:
                result.append(literal_text)
            if field_name is not None:
                try:
                    first, rest = field_name._formatter_field_name_split()
                    obj = kwargs[first]
                    for is_attr, i in rest:
                        if is_attr:
                            obj = getattr(obj, i)
                        else:
                            obj = obj[i]
                except KeyError:
                    recover = "{" + field_name
                    if conversion:
                        recover += "!" + conversion
                    if format_spec:
                        recover += ":" + format_spec
                    recover += "}"
                    result.append(recover)
                else:
                    if conversion is None:
                        pass
                    elif conversion == "s":
                        obj = str(obj)
                    elif conversion == "r":
                        obj = repr(obj)
                    else:
                        raise ValueError("Unknown conversion specifier {0!s}".format(conversion))
                    format_spec = format_str(format_spec, recursion_depth - 1)
                    result.append(format(obj, format_spec))
        return ''.join(result)

    def format_config_node(_config):
        if isinstance(_config, dict):
            for key in _config:
                _config[key] = format_config_node(_config[key])
        elif is_str(_config):
            _config = format_str(_config)
        elif isinstance(_config, list):
            for i in range(len(_config)):
                _config[i] = format_config_node(_config[i])
        return _config

    return format_config_node(config)


def print_config(config):
    return _json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))


def load_config(file_name):
    config = _json.load(open(file_name))
    if "config" not in config["input"]:
        config["input"]["config"] = file_name
    return config


def save_config(config, file_name):
    _json.dump(config, open(file_name, "w"), sort_keys=True, indent=2, separators=(',', ': '))
