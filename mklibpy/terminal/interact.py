import mklibpy.util as _util

__author__ = 'Michael'

if _util.osinfo.PYTHON2:
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


if _util.osinfo.WINDOWS:
    import msvcrt as _msvcrt


    def getch():
        """
        Get a single key from user input. Do not wait for Enter.

        Reference: http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user

        :rtype: str
        :return: The character
        """
        return _msvcrt.getch()
else:
    import sys as _sys, tty as _tty, termios as _termios


    def getch():
        """
        Get a single key from user input. Do not wait for Enter.

        Reference: http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user

        :rtype: str
        :return: The character
        """
        fd = _sys.stdin.fileno()
        old_settings = _termios.tcgetattr(fd)
        try:
            _tty.setraw(_sys.stdin.fileno())
            ch = _sys.stdin.read(1)
        finally:
            _termios.tcsetattr(fd, _termios.TCSADRAIN, old_settings)
        return ch

if _util.osinfo.LINUX:
    import readline as _readline


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
                _readline.parse_and_bind("tab: complete")
                TabAutoComplete.Bound = True
            _readline.set_completer(TabAutoComplete(*strings).complete)

        @staticmethod
        def tab(text, state):
            if state == 0:
                return text + "\t"
            else:
                return None

        @staticmethod
        def unset():
            if TabAutoComplete.Bound:
                _readline.set_completer(TabAutoComplete.tab)
