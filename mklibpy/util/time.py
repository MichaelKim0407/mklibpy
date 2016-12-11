from __future__ import absolute_import

import time as _time

__author__ = 'Michael'


def utc_now():
    return _time.gmtime()


def to_utc(t_local):
    return _time.gmtime(_time.mktime(t_local))
