"""
terminal/colored_text.py create by Michael for mklibpy package.

Colored text in terminal.
"""

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


def print_help():
    print "Usage:"
    print "    TEXT [-c COLOR] [-m MODE] [TEXT2 [-c COLOR] [-m MODE] [...]]"
    print ""
    print "List of colors:"
    for c_code in COLORS:
        print "    {}: {}".format(c_code, get_text(COLORS[c_code], color=c_code))
    print ""
    print "List of modes:"
    for m_code in MODES:
        print "    {}: {}".format(m_code, get_text(MODES[m_code], mode=m_code))


def main(args):
    result = ""
    try:
        while args:
            text = args[0]
            args = args[1:]
            if args and args[0] == "-c":
                color = args[1]
                args = args[2:]
                try:
                    color = int(color)
                except Exception:
                    pass
            else:
                color = None
            if args and args[0] == "-m":
                mode = args[1]
                args = args[2:]
                try:
                    mode = int(mode)
                except Exception:
                    pass
            else:
                mode = None
            try:
                result += get_text(text, color, mode)
            except Exception as e:
                print e
                exit(1)
    except Exception:
        print_help()
        exit(2)
    else:
        return result


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2 or "-h" in argv or "--help" in argv:
        print_help()
    else:
        print main(argv[1:])
