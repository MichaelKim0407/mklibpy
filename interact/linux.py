"""
linux.py create by Michael for mklibpy package.

Linux utility for interactive programs.
Please do not use this file directly - use mklibpy.interact instead!
"""

import os
import readline

__author__ = 'Michael'


class TabAutoComplete:
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


def clear_screen():
    os.system("clear")
