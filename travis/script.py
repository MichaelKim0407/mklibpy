from sys import version_info, stderr

import os

__author__ = 'Michael'

cwd = os.path.abspath(os.getcwd())


def cd(path):
    os.chdir(os.path.join(cwd, path))


def test():
    ret = os.system('python setup.py test')
    if ret % 256 == 0:
        ret /= 256
        ret = int(ret)
    return ret


def success(ret):
    if ret == 0:
        return True
    if ret == 5:  # no test
        return True
    return False


def test_mklibpy():
    cd('mklibpy')
    ret = test()
    if not success(ret):
        stderr.write('mklibpy test failed with return code {}\n'.format(ret))
        exit(1)


def bin_supports_version():
    return version_info.major > 2


def test_mklibpy_bin():
    if not bin_supports_version():
        return
    cd('mklibpy-bin')
    ret = test()
    if not success(ret):
        stderr.write('mklibpy-bin test failed with return code {}\n'.format(ret))
        exit(2)


if __name__ == '__main__':
    test_mklibpy()
    test_mklibpy_bin()
