import subprocess
import sys

from cached_property import cached_property, timed_cached_property

__author__ = 'Michael'


class PipUpgradeError(Exception):
    pass


class InvalidPipError(PipUpgradeError):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "'{}' is not a valid pip executable".format(self.path)


class UpgradeFailed(PipUpgradeError):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "Upgrade failed with code {}. Please upgrade manually, or fix the problem.".format(
            self.code
        )


class Pip(object):
    def __init__(self, path):
        self.path = path

    @cached_property
    def version_major(self):
        try:
            out = subprocess.check_output(
                [self.path, "--version"],
                stderr=subprocess.DEVNULL
            ).decode()
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise InvalidPipError(self.path)
        version = out.split()[1]
        major = int(version.split(".")[0])
        return major

    @timed_cached_property(ttl=60)
    def outdated(self):
        def __yield():
            try:
                cmd = [self.path, "list", "--outdated"]

                if self.version_major > 10:
                    # the legacy format has been deprecated as of pip 18
                    cmd += ['--format=freeze']
                    fmt = 'freeze'
                elif self.version_major >= 9:
                    cmd += ['--format=legacy']
                    fmt = 'legacy'
                else:
                    fmt = 'legacy'

                out = subprocess.check_output(
                    cmd,
                    stderr=subprocess.DEVNULL
                ).decode()
            except subprocess.CalledProcessError:
                raise InvalidPipError(self.path)
            for line in out.splitlines():
                line = line.strip()
                if not line:
                    continue

                if fmt == 'freeze':
                    name = line.split('==')[0]
                elif fmt == 'legacy':
                    name = line.split()[0]
                else:
                    raise ValueError(fmt)

                yield name

        return list(__yield())

    def upgrade(self, packages=None):
        if packages is None:
            packages = self.outdated
        if not packages:
            return
        try:
            subprocess.check_call(
                [self.path, "install", "-U"] + packages,
                stdout=sys.stdout,
                stderr=sys.stderr
            )
        except subprocess.CalledProcessError as e:
            raise UpgradeFailed(e.returncode)

    def all(self):
        print("--- Upgrading all packages for '{}' ---".format(self.path))
        print("{} package(s) need to be upgraded".format(len(self.outdated)))
        if not self.outdated:
            return
        print("They are: {}".format(self.outdated))

        print("Upgrading all packages...")
        self.upgrade()
        print("Upgrade successful.")


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    for pip in args:
        try:
            Pip(pip).all()
        except PipUpgradeError as e:
            print(str(e), file=sys.stderr)


if __name__ == '__main__':
    main()
