from __future__ import absolute_import

import time

__author__ = 'Michael'


def utc_now():
    return time.gmtime()


def to_utc(t_local):
    return time.gmtime(time.mktime(t_local))
