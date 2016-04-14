"""
__init__.py create by Michael for mklibpy package.

Utility for interactive programs.
"""

import platform

__author__ = 'Michael'


def print_list(l, width, columns):
    result = ""
    x = 0
    for item in l:
        s = str(item)
        d = (len(s) + 1) / width + 1
        if x + d > columns and x != 0:
            result += "\n"
            x = 0
        spec = "{{: <{}}}".format(width * d)
        s_right = spec.format(s)
        result += s_right
        x += d
    return result


def y_or_n():
    while True:
        usr_input = raw_input("Please input Y or N: ").strip()
        if usr_input == "Y":
            return True
        elif usr_input == "N":
            return False


if platform.system() == "Linux":
    from linux import *
elif platform.system() == "Windows":
    from windows import *
