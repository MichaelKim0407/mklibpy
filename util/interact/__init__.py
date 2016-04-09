"""
__init__.py create by Michael for mklibpy package.

Utility for interactive programs.
"""

import platform

__author__ = 'Michael'

if platform.system() == "Linux":
    from linux import *
