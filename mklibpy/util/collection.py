import mklibpy.error as error

__author__ = 'Michael'


def format_list(l, start="[", end="]", sep=", ", r=True, formatter=None):
    def __format_item(item):
        if formatter is None:
            if r:
                return repr(item)
            else:
                return str(item)
        else:
            return formatter(item)

    result = ""
    result += start
    for i in range(len(l)):
        if i != 0:
            result += sep
        result += __format_item(l[i])
    result += end
    return result


def format_list_multiline(l):
    return format_list(
        l,
        "[\n\t",
        "\n]",
        ",\n\t"
    )


def format_dict(
        d,
        key_width=None,
        start="{",
        end="}",
        k_v=": ",
        sep=", ",
        r_key=True,
        r_val=True,
        sort=True
):
    if key_width is None:
        key_format = "{{!{}}}".format(
            "r" if r_key else "s"
        )
    else:
        key_format = "{{!{}:<{}}}".format(
            "r" if r_key else "s",
            key_width
        )

    def __val_formatter(val):
        return repr(val) if r_val else str(val)

    def __formatter(key):
        return key_format.format(key) + k_v + __val_formatter(d[key])

    return format_list(
        sorted(d.keys()) if sort else d.keys(),
        start,
        end,
        sep,
        formatter=__formatter
    )


def format_dict_multiline(d, key_width=None, sort=True):
    return format_dict(
        d,
        key_width,
        "{\n\t",
        "\n}",
        ": ",
        ",\n\t",
        True,
        True,
        sort
    )


def to_dict(keys, values):
    """
    Combine a list of keys and a list of values into a dict.

    :param keys:
    :param values:
    :return:
    """
    if len(keys) != len(values):
        raise error.ValueSetLengthError(keys, values)
    d = {}
    for i in range(len(keys)):
        d[keys[i]] = values[i]
    return d


def union(*lists):
    """
    Find the union of lists.

    :param lists:
    :return:
    """
    result = []
    for l in lists:
        for item in l:
            if item not in result:
                result.append(item)
    return result


def intersect(*lists):
    """
    Find the intersection of lists.

    :param lists:
    :return:
    """
    result = []
    for item in lists[0]:
        for l in lists[1:]:
            if item not in l:
                break
        else:
            # item is in every list
            if item not in result:
                result.append(item)
    return result


def has_all(l1, l2):
    """
    If l1 contains every item in l2.

    :param l1:
    :param l2:
    :return:
    """
    for item in l2:
        if item not in l1:
            return False
    return True


def any(iterable, match=None):
    if match is None:
        for item in iterable:
            return True
    else:
        for item in iterable:
            if match(item):
                return True
    return False


def first(iterable, match=None):
    if match is None:
        for item in iterable:
            return item
    else:
        for item in iterable:
            if match(item):
                return item
    return None
