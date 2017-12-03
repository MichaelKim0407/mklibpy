import sys as _sys
import os as _os

DEPRECATION_WARNING = """Due to performance considerations, `import mklibpy` will not import sub-packages in v0.8.
Please directly import sub-packages.
To suppress this warning, `export __MKLIBPY_SUPPRESS_DEPRECATION_WARNING=1`,
or `import os; os.environ['__MKLIBPY_SUPPRESS_DEPRECATION_WARNING'] = '1'` before importing.
"""

if not _os.getenv('__MKLIBPY_SUPPRESS_DEPRECATION_WARNING'):
    _sys.stderr.write(DEPRECATION_WARNING)

from . import code
from . import common
from . import data
from . import error
from . import file
from . import terminal
from . import util

__author__ = 'Michael'

PACKAGES = {util, error, terminal, data, common, code, file}

__version__ = "0.7"
