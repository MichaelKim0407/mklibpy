import os
import sys
import time

from mklibpy.util.path import ensure_dir

__author__ = 'Michael'

TIME_FORMAT = '%Y-%m-%d %H:%M'


class Manager(object):
    def check(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


from .managers import builtins


def get_base_dir():
    if 'VIRTUAL_ENV' in os.environ:
        path = os.environ['VIRTUAL_ENV']
    else:
        path = os.path.expanduser('~')
    return os.path.join(path, '.upgrade-manager')


def get_config_path():
    path = os.path.join(get_base_dir(), 'config.py')
    ensure_dir(path)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('''from mklibpy.common.collection import SequenceDict
managers = SequenceDict()
''')
    return path


def get_result_path(name):
    path = os.path.join(get_base_dir(), 'results', name)
    ensure_dir(path)
    return path


def load_config(path=None):
    if path is None:
        path = get_config_path()

    vars = {}
    with open(path) as f:
        exec(f.read(), vars)
    return vars['managers']


def add(name, config_path=None):
    if config_path is None:
        config_path = get_config_path()

    builtin = builtins[name]
    cls = builtin[0]
    args = builtin[1:]

    with open(config_path, 'a') as f:
        f.write("""
### Added from builtin managers ###
from {module} import {cls}
managers['{name}'] = {cls}{args}
######
""".format(name=name, module=cls.__module__, cls=cls.__name__, args=args))


def main():
    managers = load_config()

    import argparse

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        'command',
        choices=['check', 'show', 'list', 'run', 'add'],
        help='')
    arg_parser.add_argument(
        'managers', nargs='*',
        help='''Specify upgrade managers, or leave empty for all.
Configured managers: {};
Builtin managers (can add): {}'''.format(managers.keys(), sorted(builtins)))

    args = arg_parser.parse_args()

    if args.command == 'add':
        for name in args.managers:
            if name not in builtins:
                print("'{}' is not a builtin manager".format(name), file=sys.stderr)
                continue
            add(name)
        return

    if not args.managers:
        args.managers = managers.keys()
    for name in args.managers:
        if name not in managers:
            print("'{}' is not a configured manager".format(name), file=sys.stderr)
            continue
        manager = managers[name]
        if args.command == 'check':
            sys.stdout.write("'{}' has ...".format(name))
            sys.stdout.flush()
            n = manager.check()
            sys.stdout.write("\10\10\10{} upgrade(s).\n".format(n))
            with open(get_result_path(name), 'w') as f:
                f.write("'{}' has {} upgrade(s). ({})\n".format(
                    name, n, time.strftime(TIME_FORMAT)
                ))
        elif args.command == 'show':
            with open(get_result_path(name)) as f:
                print(f.read().strip())
        elif args.command == 'list':
            print("Listing upgrades for '{}'...".format(name))
            manager.list()
        elif args.command == 'run':
            print("Upgrading '{}'...".format(name))
            manager.run()


if __name__ == '__main__':
    main()
