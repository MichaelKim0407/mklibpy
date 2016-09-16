import mklibpy.util as util

__author__ = 'Michael'

if util.osinfo.PYTHON2:
    user_input = raw_input
else:
    user_input = input


def y_or_n():
    while True:
        usr_input = user_input("Please input Y or N: ").strip()
        if usr_input == "Y":
            return True
        elif usr_input == "N":
            return False


if util.osinfo.WINDOWS:
    import msvcrt


    def getch():
        """
        Get a single key from user input. Do not wait for Enter.

        Reference: http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user

        :rtype: str
        :return: The character
        """
        return msvcrt.getch()
else:
    import sys, tty, termios


    def getch():
        """
        Get a single key from user input. Do not wait for Enter.

        Reference: http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user

        :rtype: str
        :return: The character
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

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
