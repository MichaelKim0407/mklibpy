from mklibpy.terminal.colored_text import *
from mklibpy.util.collection import format_dict

__author__ = 'Michael'


def print_help():
    def __format_dict(d):
        return format_dict(
            d,
            start="    ",
            end="",
            k_v=": ",
            sep="\n    ",
            key_width=4,
            r_key=True,
            r_val=False
        )

    _COLORS = {
        c_code: get_text(COLORS[c_code], color=c_code)
        for c_code in COLORS
    }
    _MODES = {
        m_code: get_text(MODES[m_code], mode=m_code)
        for m_code in MODES
    }
    print("""\
Usage:
    TEXT [-c COLOR] [-m MODE] [TEXT2 [-c COLOR] [-m MODE] [...]]

List of colors:
{}

List of modes:
{}
""".format(
        __format_dict(_COLORS),
        __format_dict(_MODES)
    ))


def run(args):
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
                except:
                    pass
            else:
                color = None
            if args and args[0] == "-m":
                mode = args[1]
                args = args[2:]
                try:
                    mode = int(mode)
                except:
                    pass
            else:
                mode = None
            try:
                result += get_text(text, color, mode)
            except Exception as e:
                print(e)
                exit(1)
    except:
        print_help()
        exit(2)
    else:
        return result


def main(args=None):
    if args is None:
        from sys import argv
        args = argv[1:]

    if (not args) or ("-h" in args) or ("--help" in args):
        print_help()
    else:
        print(run(args))


if __name__ == '__main__':
    main()
