# -*- coding: utf-8 -*-

"""
WRDS Python Data Access Library
==============================

WRDS-Py is a library for extracting data from WRDS data sources and getting it into Pandas.

    >>> import wrds
    >>> connection = wrds.Connection()
    >>> connection.get_libraries()
    >>> connection.get_tables('CRSP', verbose=True)
    >>> data = connection.sql('SELECT * FROM CRSP.MSI', index='DATE')
    >>> data.head()


"""

__title__ = 'wrds-py'
__version__ = '3.0'
__author__ = 'Eric Stein'
__copyright__ = '2016 Wharton Research Data Services'

import os

from .sql import Connection

