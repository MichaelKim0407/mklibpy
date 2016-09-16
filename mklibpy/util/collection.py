import mklibpy.error as error

__author__ = 'Michael'


def format_list(l, start="[", end="]", sep=", ", r=True, formatter=None):
    """
    Format a list.

    :type l: list
    :param l: The list to format
    :type start: str
    :param start:
    :type end: str
    :param end:
    :type sep: str
    :param sep:
    :type r: bool
    :param r: If formatter is not specified, whether items in the list are formatted with repr or str
    :type formatter: object -> str
    :param formatter:
    :rtype: str
    :return: The result str
    """

    if formatter is None:
        formatter = repr if r else str

    result = ""
    result += start
    for i in range(len(l)):
        if i != 0:
            result += sep
        result += formatter(l[i])
    result += end
    return result


def format_list_multiline(l):
    """
    Format a list into multiple lines.

    See also: format_list

    :type l: list
    :param l:
    :rtype: str
    :return:
    """
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
    """
    Format a dict.

    See also: format_list

    :type d: dict
    :param d: The dict to format
    :type key_width: int
    :param key_width: The minimum width for which the key is formatted with
    :type start: str
    :param start:
    :type end: str
    :param end:
    :type k_v: str
    :param k_v:
    :type sep: str
    :param sep:
    :type r_key: bool
    :param r_key: Whether keys are formatted with repr or str
    :type r_val: bool
    :param r_val: Whether values are formatted with repr or str
    :type sort: bool
    :param sort: Whether keys are sorted
    :rtype: str
    :return: The result str
    """
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
    """
    Format a dict into multiple lines.

    :type d: dict
    :param d:
    :type key_width: int
    :param key_width:
    :type sort: bool
    :param sort:
    :rtype: str
    :return:
    """
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

    :except mklibpy.error.ValueSetLengthError: The two lists do not have equal lengths.

    :type keys: list
    :param keys:
    :type values: list
    :param values:
    :rtype: list
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

    :type l1: list
    :param l1:
    :type l2: list
    :param l2:
    :rtype: bool
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
