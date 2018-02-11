__author__ = 'Michael'


class Manager(object):
    def check(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


def main():
    import argparse

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        'command',
        choices=['check', 'list', 'run', 'add'],
        help='')
    arg_parser.add_argument(
        'managers', nargs='*',
        help='Specify upgrade managers, or leave empty for all.')

    args = arg_parser.parse_args()


if __name__ == '__main__':
    main()
