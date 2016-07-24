import os

import mklibpy.util as util

from . import colored_text
from . import interact

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


if util.osinfo.LINUX or util.osinfo.MAC:
    def clear_screen():
        os.system("clear")
elif util.osinfo.WINDOWS:
    def clear_screen():
        os.system("cls")
