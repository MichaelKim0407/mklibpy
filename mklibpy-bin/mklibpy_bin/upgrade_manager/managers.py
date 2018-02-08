import re
import subprocess

from . import Manager

__author__ = 'Michael'


class AptManager(Manager):
    UP_TO_DATE = 'All packages are up to date.'
    CHECK_REGEX = re.compile('([0-9]*)(?= packages? can be upgraded.)')

    def __init__(self, apt='apt'):
        self.apt = apt

    def check(self):
        out = subprocess.check_output(
            [self.apt, 'update'],
            stderr=subprocess.DEVNULL
        ).decode()
        if self.UP_TO_DATE in out:
            return 0
        return int(self.CHECK_REGEX.findall(out)[0])

    def run(self):
        subprocess.check_call(
            [self.apt, 'upgrade', '-y']
        )


class BrewManager(Manager):
    def __init__(self, brew='brew'):
        self.brew = brew

    def update(self):
        subprocess.check_call(
            [self.brew, 'update'],
            stdout=subprocess.DEVNULL
        )

    def check(self):
        self.update()
        out = subprocess.check_output(
            [self.brew, 'outdated']
        ).decode()
        return len(out.splitlines())

    def run(self):
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

    def run(self):
        subprocess.check_call(
            [self.brew, self.cask, 'upgrade']
        )


class PipManager(Manager):
    def __init__(self, pip='pip'):
        self.pip = pip

    def check(self):
        out = subprocess.check_output(
            [self.pip, 'list', '--outdated']
        ).decode()
        if not out:
            return 0
        return len(out.splitlines()) - 2

    def run(self):
        from mklibpy_bin.pip_upgrade_all import Pip
        Pip(self.pip).all()
