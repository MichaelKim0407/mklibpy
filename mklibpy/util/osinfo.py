"""
util/osinfo.py create by Michael for mklibpy package.
"""

import platform

__author__ = 'Michael'

system = platform.system()
LINUX = system == "Linux"
WINDOWS = system == "Windows"
MAC = system == "Darwin"
