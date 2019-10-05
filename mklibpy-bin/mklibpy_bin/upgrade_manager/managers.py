import re
import subprocess

from cached_property import cached_property, timed_cached_property

from . import Manager

__author__ = 'Michael'


class AptManager(Manager):
    UP_TO_DATE = 'All packages are up to date.'
    CHECK_REGEX = re.compile('([0-9]*)(?= packages? can be upgraded.)')

    def __init__(self, apt='apt'):
        self.apt = apt

    @cached_property
    def _update_cmd(self):
        return [self.apt, 'update']

    @timed_cached_property(ttl=60)
    def _update(self):
        return subprocess.check_output(
            self._update_cmd,
            stderr=subprocess.DEVNULL
        ).decode()

    def update(self):
        return self._update

    def check(self):
        out = self.update()
        if self.UP_TO_DATE in out:
            return 0
        return int(self.CHECK_REGEX.findall(out)[0])

    @cached_property
    def _list_cmd(self):
        return [self.apt, 'list', '--upgradable']

    def list(self):
        self.update()
        subprocess.check_call(
            self._list_cmd
        )

    @cached_property
    def _upgrade_cmd(self):
        return [self.apt, 'upgrade', '-y']

    def run(self):
        self.update()
        subprocess.check_call(
            self._upgrade_cmd
        )


class BrewManager(Manager):
    def __init__(self, brew='brew'):
        self.brew = brew

    @cached_property
    def _update_cmd(self):
        return [self.brew, 'update']

    @timed_cached_property(ttl=60)
    def _update(self):
        subprocess.check_call(
            self._update_cmd,
            stdout=subprocess.DEVNULL
        )

    def update(self):
        return self._update

    @cached_property
    def _list_cmd(self):
        return [self.brew, 'outdated']

    def check(self):
        self.update()
        out = subprocess.check_output(
            self._list_cmd
        ).decode()
        return len(out.splitlines())

    def list(self):
        self.update()
        subprocess.check_call(
            self._list_cmd
        )

    @cached_property
    def _upgrade_cmd(self):
        return [self.brew, 'upgrade']

    def run(self):
        self.update()
        subprocess.check_call(
            self._upgrade_cmd
        )


class CaskManager(BrewManager):
    def __init__(self, brew='brew', cask='cask', greedy=True):
        super().__init__(brew)
        self.cask = cask
        self.greedy = greedy

    @cached_property
    def _list_cmd(self):
        return [self.brew, self.cask, 'outdated'] + (['--greedy'] if self.greedy else [])

    @cached_property
    def _upgrade_cmd(self):
        return [self.brew, self.cask, 'upgrade'] + (['--greedy'] if self.greedy else [])


class PipManager(Manager):
    def __init__(self, pip='pip'):
        from mklibpy_bin.pip_upgrade_all import Pip
        self.pip = Pip(pip)

    def check(self):
        return len(self.pip.outdated)

    @cached_property
    def _list_cmd(self):
        return [self.pip.path, 'list', '--outdated']

    def list(self):
        subprocess.call(
            self._list_cmd
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
