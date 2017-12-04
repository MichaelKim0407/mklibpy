import logging
import os

os.environ['__MKLIBPY_SUPPRESS_DEPRECATION_WARNING'] = '1'

from mklibpy.util.time import iterate_dates

__author__ = 'Michael'

DATE_FORMAT = "%Y%m%d"
LOG_FORMAT = "[%(asctime)s %(levelname)s] %(msg)s"


class RunCmdError(Exception):
    def __init__(self, date, code):
        self.date = date
        self.code = code

    def __str__(self):
        return "ERROR: {}: Exit with {}!".format(self.date, self.code)


def run_date(script, date, cmd_args=(), log_dir=None):
    cmd = "{} {}".format(script, date)
    for arg in cmd_args:
        cmd += " {!r}".format(arg)
    if log_dir:
        log_file = os.path.join(log_dir, "{}.log".format(date))
        cmd += " > {} 2>&1".format(log_file)
    logging.info("Command: '{}'".format(cmd))
    code = os.system(cmd)
    if code != 0:
        raise RunCmdError(date, code)


def run_all(script, start, end, step=1, cmd_args=(), log_dir=None, careful=False):
    for date in iterate_dates(start, end, step, date_fmt=DATE_FORMAT):
        try:
            logging.info("--- Start {} ---".format(date))
            run_date(script, date, cmd_args, log_dir)
        except RunCmdError as e:
            logging.error(str(e))
            if careful:
                raise
        finally:
            logging.info("--- End {} ---".format(date))


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    import argparse

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--log-dir",
        help='''Log file directory for script output.
                Both stdout and stderr will be directed to {date}.log.
                If none given, script output will not be directed.''')
    arg_parser.add_argument(
        "--step", '-s', type=int, default=1,
        help='Step between start date and end date')
    arg_parser.add_argument(
        "--careful", action="store_true",
        help='Abort immediately if script fails for any date')
    arg_parser.add_argument(
        "script",
        help='Script to run (the first argument must be date)')
    arg_parser.add_argument(
        "start",
        help='Start date')
    arg_parser.add_argument(
        "end",
        help='End date')
    arg_parser.add_argument(
        "cmd_args", nargs="...",
        help='Other arguments to provide to the script')

    args = arg_parser.parse_args()

    logging.info("Arguments: {}".format(args.__dict__))

    run_all(**args.__dict__)


if __name__ == '__main__':
    main()
