import platform as _platform
import sys as _sys

__author__ = 'Michael'

system = _platform.system()
LINUX = system == "Linux"
WINDOWS = system == "Windows"
MAC = system == "Darwin"

py_version = _sys.version_info
PYTHON2 = py_version.major == 2
PYTHON3 = py_version.major == 3
