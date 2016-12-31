import mklibpy.error as _error

__author__ = 'Michael'


def format_list(
        l,
        start="[",
        end="]",
        sep=", ",
        r=True,
        formatter=None
):
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


def format_list_multiline(l, **kwargs):
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
        start="[\n\t",
        end="\n]",
        sep=",\n\t",
        **kwargs
    )


def format_list_rows(
        l,
        width=None,
        columns=None,
        left=True,
        r=True,
        formatter=None
):
    if formatter is None:
        formatter = repr if r else str

    result = ""
    cur_col = 0
    for item in l:
        if cur_col >= columns and cur_col != 0:
            result += "\n"
            cur_col = 0
        s = formatter(item)
        if width is None:
            col_add = 1
            result += s + " "
        else:
            col_add = int((len(s) + 1) / width) + 1
            spec = "{{: {}{}}}".format("<" if left else ">", width * col_add)
            result += spec.format(s)
        if columns is None:
            continue
        cur_col += col_add
    return result


def format_dict(
        d,
        start="{",
        end="}",
        k_v=": ",
        sep=", ",
        sort=True,
        key_width=None,
        r_key=True,
        key_formatter=None,
        r_val=True,
        val_formatter=None
):
    """
    Format a dict.

    See also: format_list

    :type d: dict
    :param d: The dict to format
    :type start: str
    :param start:
    :type end: str
    :param end:
    :type k_v: str
    :param k_v:
    :type sep: str
    :param sep:
    :type sort: bool
    :param sort: Whether keys are sorted
    :type key_width: int
    :param key_width: The minimum width for which the key is formatted with
    :type r_key: bool
    :param r_key: Whether keys are formatted with repr or str
    :type key_formatter: obj -> str
    :param key_formatter:
    :type r_val: bool
    :param r_val: Whether values are formatted with repr or str
    :type val_formatter: obj -> str
    :param val_formatter:
    :rtype: str
    :return: The result str
    """
    if key_formatter is None:
        if key_width is None:
            key_format = "{{!{}}}".format(
                "r" if r_key else "s"
            )
        else:
            key_format = "{{!{}:<{}}}".format(
                "r" if r_key else "s",
                key_width
            )
        key_formatter = lambda key: key_format.format(key)

    if val_formatter is None:
        val_formatter = lambda val: repr(val) if r_val else str(val)

    def __formatter(key):
        return key_formatter(key) + k_v + val_formatter(d[key])

    return format_list(
        sorted(d.keys()) if sort else list(d.keys()),
        start=start,
        end=end,
        sep=sep,
        formatter=__formatter
    )


def format_dict_multiline(d, **kwargs):
    """
    Format a dict into multiple lines.

    :type d: dict
    :param d:
    :rtype: str
    :return:
    """
    return format_dict(
        d,
        start="{\n\t",
        end="\n}",
        k_v=": ",
        sep=",\n\t",
        r_key=True,
        r_val=True,
        **kwargs
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
        raise _error.ValueSetLengthError(keys, values)
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
