"""
args.py create by Michael for mklibpy package.

Utility for execution args.
"""

__author__ = 'Michael'


class OptionArg:
    def __init__(self, letter, fullname, opt_name, opt_value):
        self.letter = letter
        self.fullname = fullname
        self.opt_name = opt_name
        self.opt_value = opt_value

    def __eq__(self, other):
        return (self.letter is not None and other == self.letter) \
               or other == self.fullname

    def set(self, options):
        options[self.opt_name] = self.opt_value
