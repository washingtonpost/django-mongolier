#!/usr/bin/env python
import warnings
##
# django-mongolier
##
__title__ = 'mongolier'
__version__ = '0.4.0'
__author__ = 'Jason Bartz'
__license__ = 'MIT'
__author_email__ = ['bartzj@washpost.com']
__contributors__ = [
    'Jeremy Bowers',
]

try:
    from mongolier.db import Connection
    from mongolier.utils.convert import ConvertDecimal
except ImportError as e:
    warnings.warn(str(e))
