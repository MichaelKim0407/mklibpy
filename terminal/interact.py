"""
terminal/interact.py create by Michael for mklibpy package.

Terminal-based interactive programming.
"""

import mklibpy.util as util

__author__ = 'Michael'


def y_or_n():
    while True:
        usr_input = raw_input("Please input Y or N: ").strip()
        if usr_input == "Y":
            return True
        elif usr_input == "N":
            return False


if util.osinfo.LINUX:
    import readline


    class TabAutoComplete(object):
        Bound = False

        def __init__(self, *strings):
            self.strings = sorted(strings)

        def complete(self, text, state):
            if state == 0:
                self.matches = [
                    s for s in self.strings
                    if s.startswith(text)]
                if len(self.matches) == 1:
                    self.matches[0] += " "
            try:
                return self.matches[state]
            except IndexError:
                return None

        @staticmethod
        def set(*strings):
            if not TabAutoComplete.Bound:
                readline.parse_and_bind("tab: complete")
                TabAutoComplete.Bound = True
            readline.set_completer(TabAutoComplete(*strings).complete)

        @staticmethod
        def tab(text, state):
            if state == 0:
                return text + "\t"
            else:
                return None

        @staticmethod
        def unset():
            if TabAutoComplete.Bound:
                readline.set_completer(TabAutoComplete.tab)
