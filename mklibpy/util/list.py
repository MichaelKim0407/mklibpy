import mklibpy.error as error

__author__ = 'Michael'


def format_list(l, start="[", end="]", sep=", ", r=True):
    result = ""
    result += start
    for i in range(len(l)):
        if i != 0:
            result += sep
        result += repr(l[i]) if r else str(l[i])
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
        r_val=True
):
    l = []
    if key_width is None:
        key_format = "{{!{}}}".format(
            "r" if r_key else "s"
        )
    else:
        key_format = "{{!{}:<{}}}".format(
            "r" if r_key else "s",
            key_width
        )
    for key in sorted(d.keys()):
        item = ""
        item += key_format.format(key)
        item += k_v
        item += repr(d[key]) if r_val else str(d[key])
        l.append(item)
    return format_list(l, start, end, sep, False)


def format_dict_multiline(d, key_width=None):
    return format_dict(
        d,
        key_width,
        "{\n\t",
        "\n}",
        ": ",
        ",\n\t",
        True,
        True
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
    d = dict()
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
