"""
util/list.py create by Michael for mklibpy package.

Utility for collections.
"""

import mklibpy.error as error

__author__ = 'Michael'


def to_str(l, split=", ", start="[", end="]", fmt=repr):
    result = ""
    result += start
    for item in l[:-1]:
        result += fmt(item) + split
    result += fmt(l[-1]) + end
    return result


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
