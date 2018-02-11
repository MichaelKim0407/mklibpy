import os

from mklibpy.util.path import ensure_dir

__author__ = 'Michael'


class Manager(object):
    def check(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


def get_config_path():
    if 'VIRTUAL_ENV' in os.environ:
        path = os.environ['VIRTUAL_ENV']
    else:
        path = os.path.expanduser('~')
    path = os.path.join(path, '.upgrade-manager', 'config.py')
    ensure_dir(path)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('managers = {}\n')
    return path


def load_config(path=None):
    if path is None:
        path = get_config_path()

    vars = {}
    with open(path) as f:
        exec(f.read(), vars)
    return vars['managers']


def main():
    managers = load_config()

    import argparse

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        'command',
        choices=['check', 'list', 'run', 'add'],
        help='')
    arg_parser.add_argument(
        'managers', nargs='*',
        help='''Specify upgrade managers, or leave empty for all.
Configured managers: {}'''.format(list(managers)))

    args = arg_parser.parse_args()


if __name__ == '__main__':
    main()
