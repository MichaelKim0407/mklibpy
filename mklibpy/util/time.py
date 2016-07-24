import time

__author__ = 'michael'


def utc_now():
    return time.gmtime()


def to_utc(t_local):
    return time.gmtime(time.mktime(t_local))
