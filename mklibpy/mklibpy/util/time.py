from __future__ import absolute_import

import time as _time

__author__ = 'Michael'


def utc_now():
    return _time.gmtime()


def to_utc(t_local):
    return _time.gmtime(_time.mktime(t_local))


def iterate_dates(start, end, step=1, parallel=1, date_fmt=None):
    """
    Iterate dates.

    :type start: tuple, or str if date_fmt is provided
    :type end: tuple, or str if date_fmt is provided
    :param step: Step. Must be a positive integer if start < end,
        or a negative integer if start > end.
    :type step: int
    :param parallel: Parallelism. Must be a non-negative integer.
        If not 1, return values will be grouped by this number.
        If 0, all return values will be grouped.
    :type parallel: int
    :param date_fmt: Date format.
        If provided, `start` and `end` can be strings,
        and the return values will be formatted strings.
    :type date_fmt: str
    """
    if date_fmt is not None:
        if isinstance(start, str):
            start = _time.strptime(start, date_fmt)
        if isinstance(end, str):
            end = _time.strptime(end, date_fmt)
        for date in iterate_dates(start, end, step, parallel):
            if isinstance(date, list):
                yield [_time.strftime(date_fmt, d) for d in date]
            else:
                yield _time.strftime(date_fmt, date)
        return

    if not isinstance(parallel, int) or parallel < 0:
        raise ValueError('parallel must be a non-negative integer')

    # Fix isdst=-1 causing comparisons to fail
    start = _time.localtime(_time.mktime(start))
    end = _time.localtime(_time.mktime(end))

    if start == end:
        if parallel == 1:
            yield start
        else:
            yield [start]
        return

    if step == 0:
        raise ValueError('step cannot be 0')

    if start < end:
        if step < 0:
            raise ValueError('step must be positive for start < end')
        add = True
    else:
        if step > 0:
            raise ValueError('step must be negative for start > end')
        add = False

    if parallel == 1:
        diff = 86400 * step
        d = start
        while True:
            if d > end if add else d < end:
                break
            yield d
            d = _time.localtime(_time.mktime(d) + diff)
    else:
        n = 0
        group = []
        for date in iterate_dates(start, end, step):
            group.append(date)
            n += 1
            if n == parallel:
                yield group
                group = []
                n = 0
        if n != 0:
            yield group
