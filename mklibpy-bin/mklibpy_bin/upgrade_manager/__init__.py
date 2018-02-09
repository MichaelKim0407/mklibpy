__author__ = 'Michael'


class Manager(object):
    def check(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
