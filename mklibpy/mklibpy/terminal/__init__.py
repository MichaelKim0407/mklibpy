import os as _os

from . import (  # noqa: F401
    colored_text,
    interact,
)
from .. import (
    util as _util,
)

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


if _util.osinfo.LINUX or _util.osinfo.MAC:
    def clear_screen():
        _os.system("clear")
elif _util.osinfo.WINDOWS:
    def clear_screen():
        _os.system("cls")
