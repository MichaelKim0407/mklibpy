import sys
from subprocess import check_call, check_output, CalledProcessError, DEVNULL

__author__ = 'Michael'

PIP_MIN_VERSION = 9


class PipUpgradeError(Exception):
    pass


class InvalidPipError(PipUpgradeError):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "'{}' is not a valid pip executable".format(self.path)


class PipVersionError(PipUpgradeError):
    def __init__(self, path, version):
        self.path = path
        self.version = version

    def __str__(self):
        return "'{}' version is {}; at least {} is required".format(
            self.path,
            self.version,
            PIP_MIN_VERSION
        )


class UpgradeFailed(PipUpgradeError):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "Upgrade failed with code {}. Please upgrade manually, or fix the problem.".format(
            self.code
        )


class Pip(object):
    def __init__(self, path):
        self.__path = path
        self.__outdated = []

    def check_version(self):
        try:
            out = check_output(
                [self.__path, "--version"],
                stderr=DEVNULL
            ).decode()
        except (FileNotFoundError, CalledProcessError):
            raise InvalidPipError(self.__path)
        version = out.split()[1]
        major = int(version.split(".")[0])
        if major < PIP_MIN_VERSION:
            raise PipVersionError(self.__path, version)

    def list_outdated(self):
        def __yield():
            try:
                out = check_output(
                    [self.__path, "list", "--outdated"],
                    stderr=DEVNULL
                ).decode()
            except CalledProcessError:
                raise InvalidPipError(self.__path)
            for line in out.splitlines()[2:]:
                line = line.strip()
                if not line:
                    continue
                name = line.split()[0]
                yield name

        self.__outdated = list(__yield())
        return self.__outdated

    def upgrade(self, packages=None):
        if packages is None:
            packages = self.__outdated
        try:
            check_call(
                [self.__path, "install", "-U"] + packages,
                stdout=sys.stdout,
                stderr=sys.stderr
            )
        except CalledProcessError as e:
            raise UpgradeFailed(e.returncode)

    def all(self):
        print("--- Upgrading all packages for '{}' ---".format(self.__path))
        self.check_version()

        self.list_outdated()
        print("{} package(s) need to be upgraded".format(len(self.__outdated)))
        if not self.__outdated:
            return
        print("They are: {}".format(self.__outdated))

        print("Upgrading all packages...")
        self.upgrade()
        print("Upgrade successful.")


def main(args=None):
    if not args:
        args = sys.argv[1:]

    for pip in args:
        try:
            Pip(pip).all()
        except PipUpgradeError as e:
            print(str(e), file=sys.stderr)


if __name__ == '__main__':
    main()
