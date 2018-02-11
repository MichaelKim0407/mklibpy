# mklibpy-bin: Command line executables for mklibpy

Author: [Michael Kim](http://michaelkim0407.com) <mkim0407@gmail.com>

## Compatibility

Although `mklibpy` supports Python 2.7, this executable package only supports Python 3.

## Installation

```
pip3 install mklibpy-bin
```

# List of commands

* `colored`

    Print colored text in the terminal.

    Pass `--help` to see detailed usage.

* `dates`

    Execute a series of commands based on dates.

    Pass `--help` to see detailed usage.

* `ls-git`

    Replace `ls` with `ls-git` and pass arguments as normal.

    If `-l` option is specified, git-branch will be appended if the directory is the root directory of a git repo.

    If in colored mode (`--color` for GNU ls or `-G` for BSD ls), git-branch will also be colored.

* `pip-upgrade-all`

    Upgrade all packages for a `pip` installation.

    Pass `pip` executables as arguments (either /path/to/pip or just pip if it's under $PATH).

* `upgrade`

    Manage upgrades on your environment.

    Builtin managers for `apt`, `brew`, `brew cask`, `pip2` and `pip3`.

    Supports virtualenv.

    You can also write your own managers in the configuration file, found at `~/.upgrade-manager/config.py` or `$VIRTUAL_ENV/.upgrade-manager.config.py`.
