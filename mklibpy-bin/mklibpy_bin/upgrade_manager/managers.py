import re
import subprocess

from cached_property import timed_cached_property

from . import Manager

__author__ = 'Michael'


class AptManager(Manager):
    UP_TO_DATE = 'All packages are up to date.'
    CHECK_REGEX = re.compile('([0-9]*)(?= packages? can be upgraded.)')

    def __init__(self, apt='apt'):
        self.apt = apt

    @timed_cached_property(ttl=60)
    def __update(self):
        return subprocess.check_output(
            [self.apt, 'update'],
            stderr=subprocess.DEVNULL
        ).decode()

    def update(self):
        return self.__update

    def check(self):
        out = self.update()
        if self.UP_TO_DATE in out:
            return 0
        return int(self.CHECK_REGEX.findall(out)[0])

    def list(self):
        self.update()
        subprocess.check_call(
            [self.apt, 'list', '--upgradable']
        )

    def run(self):
        self.update()
        subprocess.check_call(
            [self.apt, 'upgrade', '-y']
        )


class BrewManager(Manager):
    def __init__(self, brew='brew'):
        self.brew = brew

    @timed_cached_property(ttl=60)
    def __update(self):
        subprocess.check_call(
            [self.brew, 'update'],
            stdout=subprocess.DEVNULL
        )

    def update(self):
        return self.__update

    def check(self):
        self.update()
        out = subprocess.check_output(
            [self.brew, 'outdated']
        ).decode()
        return len(out.splitlines())

    def list(self):
        self.update()
        subprocess.check_call(
            [self.brew, 'outdated']
        )

    def run(self):
        self.update()
        subprocess.check_call(
            [self.brew, 'upgrade']
        )


class CaskManager(BrewManager):
    def __init__(self, brew='brew', cask='cask'):
        super().__init__(brew)
        self.cask = cask

    def check(self):
        self.update()
        out = subprocess.check_output(
            [self.brew, self.cask, 'outdated']
        ).decode()
        return len(out.splitlines())

    def list(self):
        self.update()
        subprocess.check_call(
            [self.brew, self.cask, 'outdated']
        )

    def run(self):
        self.update()
        subprocess.check_call(
            [self.brew, self.cask, 'upgrade']
        )


class PipManager(Manager):
    def __init__(self, pip='pip'):
        from mklibpy_bin.pip_upgrade_all import Pip
        self.pip = Pip(pip)

    def check(self):
        return len(self.pip.outdated)

    def list(self):
        subprocess.call(
            [self.pip.path, 'list', '--outdated']
        )

    def run(self):
        self.pip.upgrade()


builtins = {
    'pip2': (PipManager, 'pip2'),
    'pip3': (PipManager, 'pip3'),
    'apt': (AptManager,),
    'brew': (BrewManager,),
    'cask': (CaskManager,),
}
