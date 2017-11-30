import re as _re

__author__ = 'Michael'

COLORS = {
    30: "black",
    31: "red",
    32: "green",
    33: "yellow",
    34: "blue",
    35: "magenta",
    36: "cyan",
    37: "gray"
}

MODES = {
    0: "default",
    1: "bold",
    2: "dark",
    4: "underline",
    7: "fill",
    9: "strike"
}

__switch_reg = _re.compile('\033\[[0-9;]*m')


def get_color_code(color):
    color = color.lower()
    for code in COLORS:
        if COLORS[code] == color:
            return code
    return -1


def get_mode_code(mode):
    mode = mode.lower()
    for code in MODES:
        if MODES[code] == mode:
            return code
    return -1


def get_switch(color=None, mode=None):
    if mode is None:
        m_code = 0
    elif isinstance(mode, int):
        m_code = mode
    else:
        m_code = get_mode_code(mode)
    if color is None:
        return "\033[{}m".format(m_code)
    elif isinstance(color, int):
        c_code = color
    else:
        c_code = get_color_code(color)
    return "\033[{};{}m".format(m_code, c_code)


def get_text(text, color=None, mode=None):
    return get_switch(color, mode) + text + get_switch()


def remove_switch(text):
    return __switch_reg.sub('', text)


class ColoredText(object):
    def __init__(self, text, color=None, mode=None):
        self.text = text
        self.color = color
        self.mode = mode
        self.result = get_text(text, color, mode)

    def __repr__(self):
        return self.result

    def __str__(self):
        return self.result
